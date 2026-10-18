"""
AgroGen AI — Dataset Split Image Renamer
Renames all images inside ml/disease_detection/dataset_split/
so each image is explicitly labeled with its crop, class name, split, and index.
Format: {crop}_{class_name}_{split}_{index:05d}.{ext}
"""

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SPLIT_DIR = BASE_DIR / "dataset_split"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}


def clean_name(name: str) -> str:
    """Sanitize directory names into clean snake_case identifiers."""
    cleaned = re.sub(r"[^\w\-]+", "_", name).strip("_")
    # Collapse multiple consecutive underscores
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned


def rename_images_in_dataset_split():
    if not SPLIT_DIR.exists():
        print(f"Error: {SPLIT_DIR} does not exist!")
        sys.exit(1)

    crops = sorted([c for c in SPLIT_DIR.iterdir() if c.is_dir()])
    print(f"Found {len(crops)} crop folders to process in {SPLIT_DIR.name}.")

    total_renamed = 0

    for crop in crops:
        crop_clean = clean_name(crop.name)
        crop_count = 0
        classes = sorted([d for d in crop.iterdir() if d.is_dir()])

        for cls_dir in classes:
            cls_clean = clean_name(cls_dir.name)
            # Prefix with crop name if the class name doesn't already contain it
            if crop_clean.lower() not in cls_clean.lower():
                base_label = f"{crop_clean}_{cls_clean}"
            else:
                base_label = cls_clean

            for split in ["train", "test", "validation"]:
                split_dir = cls_dir / split
                if not split_dir.exists() or not split_dir.is_dir():
                    continue

                # Collect all valid image files
                image_files = [
                    f for f in split_dir.iterdir()
                    if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
                ]

                if not image_files:
                    continue

                # Pass 1: rename to temporary names to avoid any naming collisions
                temp_records = []
                for i, img_path in enumerate(image_files, 1):
                    ext = img_path.suffix.lower()
                    temp_path = split_dir / f"__temp_{i}{ext}"
                    os.replace(img_path, temp_path)
                    temp_records.append((temp_path, ext))

                # Pass 2: rename to final standardized labeled format
                for i, (temp_path, ext) in enumerate(temp_records, 1):
                    final_name = split_dir / f"{base_label}_{split}_{i:05d}{ext}"
                    os.replace(temp_path, final_name)
                    crop_count += 1

        total_renamed += crop_count
        print(f"[{crop.name}] Finished: {crop_count} images labeled.")

    print(f"\nAll done! Total images renamed and labeled: {total_renamed}")


if __name__ == "__main__":
    rename_images_in_dataset_split()
