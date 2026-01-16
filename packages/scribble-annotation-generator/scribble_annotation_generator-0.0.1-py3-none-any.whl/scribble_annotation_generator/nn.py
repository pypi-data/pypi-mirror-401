# ============================================================
# Scribble Annotation Generation
# - Autoregressive Count Model
# - Set-Transformer Object Generator
# - Hungarian Matching Loss
# - PyTorch Lightning
# ============================================================

import math
import os
from typing import Dict, Optional, Tuple

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl

from scipy.optimize import linear_sum_assignment
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint

from scribble_annotation_generator.dataset import ScribbleDataset
from scribble_annotation_generator.utils import (
    generate_multiclass_scribble,
    unpack_feature_vector,
)


# ============================================================
# Utility
# ============================================================


def masked_mean(x, mask, dim=1, eps=1e-6):
    mask = mask.float()
    return (x * mask.unsqueeze(-1)).sum(dim) / (mask.sum(dim, keepdim=True) + eps)


# ============================================================
# Autoregressive Count Model
# p(n1, n2, ..., nC)
# ============================================================


class CountModel(pl.LightningModule):
    """
    Models joint distribution over object counts per class.
    Autoregressive over classes.
    """

    def __init__(self, num_classes: int, hidden_dim=128, max_count=20):
        super().__init__()
        self.num_classes = num_classes
        self.max_count = max_count

        self.embedding = nn.Embedding(max_count + 1, hidden_dim)

        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim * num_classes, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, (max_count + 1) * num_classes),
        )

    def forward(self, counts):
        """
        counts: (B, C) integer tensor
        """
        B, C = counts.shape
        embeds = self.embedding(counts)  # (B, C, D)
        flat = embeds.view(B, -1)  # (B, C*D)
        logits = self.mlp(flat)  # (B, C*(K+1))
        logits = logits.view(B, C, self.max_count + 1)
        return logits

    def training_step(self, batch, batch_idx):
        counts = batch["counts"]  # (B, C)
        logits = self(counts)
        loss = F.cross_entropy(
            logits.view(-1, self.max_count + 1),
            counts.view(-1),
        )
        self.log("count_loss", loss)
        return loss

    def sample(self, batch_size=1):
        counts = torch.zeros(batch_size, self.num_classes, dtype=torch.long)
        for c in range(self.num_classes):
            logits = self(counts)[:, c]
            probs = F.softmax(logits, dim=-1)
            counts[:, c] = torch.multinomial(probs, 1).squeeze(-1)
        return counts

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)


# ============================================================
# Set Transformer Blocks
# ============================================================


class MAB(nn.Module):
    def __init__(self, dim, num_heads):
        super().__init__()
        self.attn = nn.MultiheadAttention(dim, num_heads, batch_first=True)
        self.ff = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, dim),
        )
        self.ln1 = nn.LayerNorm(dim)
        self.ln2 = nn.LayerNorm(dim)

    def forward(self, Q, K, mask=None):
        attn, _ = self.attn(Q, K, K, key_padding_mask=mask)
        Q = self.ln1(Q + attn)
        Q = self.ln2(Q + self.ff(Q))
        return Q


class SAB(nn.Module):
    def __init__(self, dim, num_heads):
        super().__init__()
        self.mab = MAB(dim, num_heads)

    def forward(self, X, mask=None):
        return self.mab(X, X, mask)


class PMA(nn.Module):
    def __init__(self, dim, num_heads, num_seeds):
        super().__init__()
        self.seed = nn.Parameter(torch.randn(1, num_seeds, dim))
        self.mab = MAB(dim, num_heads)

    def forward(self, X, mask=None):
        B = X.size(0)
        seed = self.seed.expand(B, -1, -1)
        return self.mab(seed, X, mask)


class ObjectEncoder(nn.Module):
    def __init__(self, dim, num_heads, num_layers):
        super().__init__()
        self.layers = nn.ModuleList([SAB(dim, num_heads) for _ in range(num_layers)])

    def forward(self, X, mask=None):
        for layer in self.layers:
            X = layer(X, mask)
        return X


class MDNCrossAttentionDecoder(nn.Module):
    """
    Transformer decoder with Mixture Density Network (MDN) output.
    """

    def __init__(
        self,
        hidden_dim: int,
        obj_dim: int,
        num_components: int = 5,
        latent_dim: int = 8,
        num_heads: int = 4,
        num_layers: int = 2,
    ):
        super().__init__()

        self.K = num_components
        self.obj_dim = obj_dim
        self.latent_dim = latent_dim

        self.latent_proj = nn.Linear(latent_dim, hidden_dim)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            batch_first=True,
        )
        self.decoder = nn.TransformerDecoder(
            decoder_layer,
            num_layers=num_layers,
        )

        # Mixture heads
        self.pi_head = nn.Linear(hidden_dim, self.K)
        self.mu_head = nn.Linear(hidden_dim, self.K * obj_dim)
        self.log_var_head = nn.Linear(hidden_dim, self.K * obj_dim)

    def forward(
        self,
        memory,  # (B, N, D)
        memory_mask,  # (B, N)
        query_embed,  # (B, D)
        z=None,  # (B, latent_dim)
    ):
        B = memory.size(0)

        if z is None:
            z = torch.randn(B, self.latent_dim, device=memory.device)

        query = query_embed + self.latent_proj(z)
        query = query.unsqueeze(1)  # (B, 1, D)

        out = self.decoder(
            tgt=query,
            memory=memory,
            memory_key_padding_mask=(memory_mask == 0),
        )[
            :, 0
        ]  # (B, D)

        pi_logits = self.pi_head(out)  # (B, K)
        mu = self.mu_head(out).view(B, self.K, self.obj_dim)
        log_var = self.log_var_head(out).view(B, self.K, self.obj_dim)

        log_var = log_var.clamp(-6.0, 3.0)

        return pi_logits, mu, log_var


# ============================================================
# Object Generator Model
# ============================================================


class ObjectGenerator(pl.LightningModule):
    """
    Masked-object autoregressive generator with Hungarian matching.
    """

    def __init__(
        self,
        num_classes: int,
        obj_dim: int,
        hidden_dim=128,
        num_heads=4,
        num_encoder_layers=2,
        num_decoder_layers=2,
    ):
        super().__init__()

        self.num_classes = num_classes
        self.obj_dim = obj_dim

        self.class_embed = nn.Embedding(num_classes, hidden_dim)
        self.obj_embed = nn.Linear(obj_dim, hidden_dim)

        self.encoder = ObjectEncoder(
            dim=hidden_dim, num_heads=num_heads, num_layers=num_encoder_layers
        )

        self.decoder = MDNCrossAttentionDecoder(
            hidden_dim=hidden_dim,
            obj_dim=obj_dim,
            latent_dim=8,
            num_heads=num_heads,
            num_layers=num_decoder_layers,
        )

    # --------------------------------------------------------

    def forward(self, objs, classes, mask, query_class):
        """
        objs: (B, N, obj_dim)
        classes: (B, N)
        mask: (B, N) 1=present, 0=masked
        query_class: (B,)
        """

        obj_emb = self.obj_embed(objs)
        class_emb = self.class_embed(classes)
        x = obj_emb + class_emb

        enc = self.encoder(x, mask=(mask == 0))
        query_emb = self.class_embed(query_class)

        pi_logits, mu, log_var = self.decoder(
            memory=enc,
            memory_mask=mask,
            query_embed=query_emb,
        )

        return pi_logits, mu, log_var

    # --------------------------------------------------------

    def hungarian_mdn_loss(self, pi_logits, mu, log_var, targets):
        """
        pi_logits: (B, K)
        mu:        (B, K, D)
        log_var:   (B, K, D)
        targets:   (B, T, D)
        """

        total_loss = 0.0
        B = mu.size(0)

        for i in range(B):
            t = targets[i]  # (T, D)

            costs = []
            for obj in t:
                obj = obj.unsqueeze(0)
                cost = self.mdn_nll(
                    pi_logits[i : i + 1],
                    mu[i : i + 1],
                    log_var[i : i + 1],
                    obj,
                )
                costs.append(cost)

            cost = torch.stack(costs).detach().cpu().numpy()
            row, col = linear_sum_assignment(cost.reshape(1, -1))
            matched = t[col[0]].unsqueeze(0)

            total_loss += self.mdn_nll(
                pi_logits[i : i + 1],
                mu[i : i + 1],
                log_var[i : i + 1],
                matched,
            )

        return total_loss / B

    # --------------------------------------------------------

    def training_step(self, batch, batch_idx):
        objs = batch["objects"]  # (B, N, D)
        classes = batch["classes"]  # (B, N)
        mask = batch["mask"]  # (B, N)
        target_objs = batch["targets"]  # (B, K, D)
        query_class = batch["query_cls"]  # (B,)

        pi_logits, mu, log_var = self(objs, classes, mask, query_class)
        loss = self.hungarian_mdn_loss(pi_logits, mu, log_var, target_objs)

        self.log("obj_loss", loss)
        return loss

    # --------------------------------------------------------

    def validation_step(self, batch, batch_idx):
        objs = batch["objects"]  # (B, N, D)
        classes = batch["classes"]  # (B, N)
        mask = batch["mask"]  # (B, N)
        target_objs = batch["targets"]  # (B, K, D)
        query_class = batch["query_cls"]  # (B,)

        pi_logits, mu, log_var = self(objs, classes, mask, query_class)
        loss = self.hungarian_mdn_loss(pi_logits, mu, log_var, target_objs)

        self.log("val_loss", loss, prog_bar=True)
        return loss

    # --------------------------------------------------------

    def mdn_nll(self, pi_logits, mu, log_var, target):
        """
        pi_logits: (B, K)
        mu:        (B, K, D)
        log_var:   (B, K, D)
        target:    (B, D)
        """

        B, K, D = mu.shape

        target = target.unsqueeze(1)  # (B, 1, D)

        log_pi = F.log_softmax(pi_logits, dim=-1)  # (B, K)

        log_prob = -0.5 * (
            log_var + (target - mu).pow(2) / log_var.exp() + math.log(2 * math.pi)
        ).sum(
            dim=-1
        )  # (B, K)

        log_mix = torch.logsumexp(log_pi + log_prob, dim=-1)

        return -log_mix.mean()

    # --------------------------------------------------------

    @torch.no_grad()
    def sample_from_mdn(self, pi_logits, mu, log_var, temperature=1.0):
        """
        Returns one sampled object per batch element.
        """

        pi = F.softmax(pi_logits / temperature, dim=-1)  # (B, K)
        comp = torch.multinomial(pi, 1).squeeze(-1)  # (B,)

        B = mu.size(0)
        idx = torch.arange(B)

        sel_mu = mu[idx, comp]
        sel_std = log_var[idx, comp].exp().sqrt() * temperature

        random_vector = torch.randn_like(sel_mu)
        random_vector[:, 2] = random_vector[:, 0]
        random_vector[:, 3] = random_vector[:, 1]

        return sel_mu + random_vector * sel_std

    # --------------------------------------------------------

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-4)


# ============================================================
# Inference
# ============================================================


def generate_scribble(
    model: ObjectGenerator,
    objects: torch.Tensor,
    classes: torch.Tensor,
    mask: torch.Tensor,
    colour_map: Dict[Tuple[int, int, int], int],
    i: int,
    output_dir: str,
) -> np.ndarray:
    os.makedirs(output_dir, exist_ok=True)
    index = mask.argmin().item()

    original = generate_multiclass_scribble(
        image_shape=(512, 512),
        objects=[unpack_feature_vector(obj) for obj in objects.numpy()],
        classes=classes.numpy(),
        colour_map=colour_map,
    )

    # Save the original scribble
    output_path = os.path.join(output_dir, f"{i}_original.png")

    # Convert RGB to BGR for saving with OpenCV
    original_bgr = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_path), original_bgr)

    classes_removed = classes.clone()
    classes_removed[index:] = 0
    synthetic = generate_multiclass_scribble(
        image_shape=(512, 512),
        objects=[unpack_feature_vector(obj) for obj in objects.numpy()],
        classes=classes_removed.numpy(),
        colour_map=colour_map,
    )

    # Save the synthetic scribble
    output_path = os.path.join(output_dir, f"{i}_synthetic_removed.png")

    # Convert RGB to BGR for saving with OpenCV
    synthetic_bgr = cv2.cvtColor(synthetic, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_path), synthetic_bgr)

    while index < len(classes) and classes[index] != 0:
        with torch.no_grad():
            pi_logits, mu, log_var = model(
                objects[None],
                classes[None],
                mask[None],
                classes[index : index + 1],
            )
            sample = model.sample_from_mdn(pi_logits, mu, log_var, temperature=1.0)[0]

        objects[index] = sample
        mask[index] = 1
        index += 1

    print(objects)

    synthetic = generate_multiclass_scribble(
        image_shape=(512, 512),
        objects=[unpack_feature_vector(obj) for obj in objects.numpy()],
        classes=classes.numpy(),
        colour_map=colour_map,
    )

    # Save the synthetic scribble
    output_path = os.path.join(output_dir, f"{i}_synthetic.png")

    # Convert RGB to BGR for saving with OpenCV
    synthetic_bgr = cv2.cvtColor(synthetic, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_path), synthetic_bgr)


# ============================================================
# Training Entry Point
# ============================================================

def train_and_infer(
    train_dir: str,
    val_dir: str,
    colour_map: Dict[Tuple[int, int, int], int],
    checkpoint_dir: str = "./local/nn-checkpoints",
    inference_dir: str = "./local/nn-inference",
    batch_size: int = 8,
    num_workers: int = 4,
    max_epochs: int = 50,
    num_classes: Optional[int] = None,
):
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(inference_dir, exist_ok=True)

    resolved_num_classes = (
        num_classes if num_classes is not None else len(set(colour_map.values()))
    )

    train_dataset = ScribbleDataset(
        num_classes=resolved_num_classes, data_dir=train_dir, colour_map=colour_map
    )
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=True,
        prefetch_factor=2,
    )

    val_dataset = ScribbleDataset(
        num_classes=resolved_num_classes, data_dir=val_dir, colour_map=colour_map
    )
    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=1,
        num_workers=num_workers,
        shuffle=False,
        prefetch_factor=2,
    )

    obj_dim = train_dataset[0]["objects"].shape[1]

    obj_model = ObjectGenerator(
        num_classes=resolved_num_classes,
        obj_dim=obj_dim,
        hidden_dim=256,
        num_encoder_layers=4,
        num_decoder_layers=4,
    )

    early_stop = EarlyStopping(monitor="val_loss", mode="min", verbose=True)
    checkpoint = ModelCheckpoint(
        monitor="val_loss",
        mode="min",
        save_top_k=1,
        dirpath=checkpoint_dir,
        filename="best-checkpoint",
    )

    trainer = pl.Trainer(max_epochs=max_epochs, callbacks=[early_stop, checkpoint])
    trainer.fit(obj_model, train_dataloaders=train_loader, val_dataloaders=val_loader)

    for i in range(len(val_dataset)):
        datum = val_dataset[i]
        objects = datum["objects"]
        classes = datum["classes"]
        mask = datum["mask"]
        generate_scribble(
            obj_model,
            objects=objects,
            classes=classes,
            mask=mask,
            colour_map=colour_map,
            i=i,
            output_dir=inference_dir,
        )
