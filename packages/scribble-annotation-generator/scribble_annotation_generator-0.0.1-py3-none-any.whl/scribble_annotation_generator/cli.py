import argparse
import os
from typing import Dict, Tuple

from scribble_annotation_generator.crop_field import (
    NUM_SAMPLES_TO_GENERATE,
    generate_crop_field_dataset,
)
from scribble_annotation_generator.nn import train_and_infer


def parse_colour_map(value: str) -> Dict[Tuple[int, int, int], int]:
    """Parse a colour map from an inline string or a file path."""

    def _validate_rgb(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = rgb
        for channel in (r, g, b):
            if channel < 0 or channel > 255:
                raise ValueError("RGB values must be between 0 and 255")
        return rgb

    mapping: Dict[Tuple[int, int, int], int] = {}

    if os.path.isfile(value):
        with open(value, "r", encoding="utf-8") as handle:
            for idx, line in enumerate(handle):
                stripped = line.strip()
                if not stripped:
                    continue
                parts = [part.strip() for part in stripped.split(",") if part.strip()]
                if len(parts) == 4:
                    r, g, b, cls = parts
                elif len(parts) == 3:
                    r, g, b = parts
                    cls = idx
                else:
                    raise ValueError(
                        "Each line in the colour map file must have 3 (RGB) or 4 (RGB,class) comma-separated values"
                    )
                rgb = _validate_rgb((int(r), int(g), int(b)))
                mapping[rgb] = int(cls)
    else:
        entries = [entry.strip() for entry in value.split(";") if entry.strip()]
        for entry in entries:
            if "=" in entry:
                colour_part, class_part = entry.split("=", 1)
            elif ":" in entry:
                colour_part, class_part = entry.split(":", 1)
            else:
                raise ValueError(
                    "Inline colour map entries must separate colour and class with '=' or ':'"
                )
            rgb_parts = [part.strip() for part in colour_part.split(",") if part.strip()]
            if len(rgb_parts) != 3:
                raise ValueError("Colours must be provided as R,G,B")
            rgb = _validate_rgb((int(rgb_parts[0]), int(rgb_parts[1]), int(rgb_parts[2])))
            mapping[rgb] = int(class_part.strip())

    if not mapping:
        raise ValueError("No colours were parsed for the colour map")

    return mapping


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scribble Annotation Generator CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    crop_parser = subparsers.add_parser(
        "crop-field", help="Generate synthetic crop field scribble images."
    )
    crop_parser.add_argument(
        "--output-dir",
        default="./local/crop_field",
        help="Directory to write generated crop field images.",
    )
    crop_parser.add_argument(
        "--num-samples",
        type=int,
        default=NUM_SAMPLES_TO_GENERATE,
        help="Number of images to generate.",
    )
    crop_parser.add_argument(
        "--min-rows",
        type=int,
        default=4,
        help="Minimum number of crop rows per sample.",
    )
    crop_parser.add_argument(
        "--max-rows",
        type=int,
        default=6,
        help="Maximum number of crop rows per sample.",
    )
    crop_parser.add_argument(
        "--colour-map",
        required=True,
        help=(
            "Colour map specified inline as 'R,G,B=class;...' or a path to a file "
            "with one 'R,G,B,class' entry per line."
        ),
    )

    train_parser = subparsers.add_parser(
        "train-nn", help="Train the scribble object generator and run inference."
    )
    train_parser.add_argument(
        "--train-dir",
        required=True,
        help="Path to the training dataset directory.",
    )
    train_parser.add_argument(
        "--val-dir",
        required=True,
        help="Path to the validation dataset directory.",
    )
    train_parser.add_argument(
        "--checkpoint-dir",
        default="./local/nn-checkpoints",
        help="Directory to save model checkpoints.",
    )
    train_parser.add_argument(
        "--inference-dir",
        default="./local/nn-inference",
        help="Directory to save inference visualisations.",
    )
    train_parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Batch size for training.",
    )
    train_parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of worker processes for data loading.",
    )
    train_parser.add_argument(
        "--max-epochs",
        type=int,
        default=50,
        help="Maximum number of training epochs.",
    )
    train_parser.add_argument(
        "--num-classes",
        type=int,
        default=None,
        help="Override the number of classes; defaults to the number of unique class IDs in the colour map.",
    )
    train_parser.add_argument(
        "--colour-map",
        required=True,
        help=(
            "Colour map specified inline as 'R,G,B=class;...' or a path to a file "
            "with one 'R,G,B,class' entry per line."
        ),
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    colour_map = parse_colour_map(args.colour_map)

    if args.command == "crop-field":
        generate_crop_field_dataset(
            output_dir=args.output_dir,
            colour_map=colour_map,
            num_samples=args.num_samples,
            min_rows=args.min_rows,
            max_rows=args.max_rows,
        )
    elif args.command == "train-nn":
        train_and_infer(
            train_dir=args.train_dir,
            val_dir=args.val_dir,
            colour_map=colour_map,
            checkpoint_dir=args.checkpoint_dir,
            inference_dir=args.inference_dir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            max_epochs=args.max_epochs,
            num_classes=args.num_classes,
        )
    else:
        parser.error("A subcommand is required.")


if __name__ == "__main__":
    main()
