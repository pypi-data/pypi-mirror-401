import os
import random

import cv2
import torch
import torch.nn.functional as F

from scribble_annotation_generator.utils import (
    extract_class_masks,
    extract_object_features,
    get_objects,
    rgb_to_indexed,
)


class ScribbleDataset(torch.utils.data.Dataset):
    def __init__(
        self, num_classes, data_dir, colour_map=None, max_objects=50, late_shift=False
    ):
        self.data_dir = data_dir
        self.filenames = sorted(os.listdir(data_dir))
        self.num_classes = num_classes
        self.colour_map = colour_map
        self.max_objects = max_objects
        self.late_shift = late_shift

        if len(self.filenames) == 0:
            raise ValueError(f"No files found in {data_dir}")

        # Auto-detect format from first image
        first_image_path = os.path.join(self.data_dir, self.filenames[0])
        first_img = cv2.imread(first_image_path, cv2.IMREAD_UNCHANGED)
        if first_img is not None:
            self.is_rgb = len(first_img.shape) == 3 and first_img.shape[2] >= 3
        else:
            raise IOError(f"Could not read {first_image_path}")

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        filepath = os.path.join(self.data_dir, self.filenames[idx])

        if self.is_rgb:
            if self.colour_map is None:
                raise ValueError("colour_map must be provided for RGB annotations")

            mask = cv2.imread(str(filepath), cv2.IMREAD_COLOR)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            mask = rgb_to_indexed(mask, self.colour_map)
        else:
            mask = cv2.imread(str(filepath), cv2.IMREAD_GRAYSCALE)

        objects = []
        classes = []
        class_masks = extract_class_masks(mask)

        for class_id, class_mask in class_masks.items():
            class_objects = get_objects(class_mask)
            objects.extend(class_objects)
            classes.extend([class_id] * len(class_objects))

        objects = [extract_object_features(obj) for obj in objects]

        permutation = list(range(len(objects)))
        random.shuffle(permutation)

        objects = torch.stack([objects[i] for i in permutation])
        classes = torch.tensor([classes[i] for i in permutation])

        # Mask everything after a random point
        if self.late_shift:
            mask_start = random.randint((len(objects) // 4) * 3, len(objects) - 1)
        else:
            mask_start = random.randint(1, len(objects) - 1)
        mask = torch.ones(len(objects))
        mask[mask_start:] = 0

        query_cls = classes[mask_start]
        targets = objects[classes == query_cls, :]

        objects = F.pad(objects, (0, 0, 0, self.max_objects - len(objects)), value=0)
        classes = F.pad(classes, (0, self.max_objects - len(classes)), value=0)
        mask = F.pad(mask, (0, self.max_objects - len(mask)), value=0)
        targets = F.pad(
            targets, (0, 0, 0, self.max_objects - targets.size(0)), value=1e7
        )

        return {
            "objects": objects,
            "classes": classes,
            "mask": mask,
            "query_cls": query_cls,
            "targets": targets,
            "counts": torch.bincount(classes, minlength=self.num_classes),
        }
