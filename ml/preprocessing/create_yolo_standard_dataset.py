"""
AgroGen AI — Build YOLO-Standard-Dataset
Moves all 95 classes across all 16 crops from dataset_split/
into a single unified YOLO Classification dataset structure:

YOLO-Standard-Dataset/
   ├── train/
   │     ├── <class_1>/
   │     └── <class_95>/
   ├── val/
   │     ├── <class_1>/
   │     └── <class_95>/
   └── test/
         ├── <class_1>/
         └── <class_95>/
"""

import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "dataset_split"
DEST_DIR = BASE_DIR / "YOLO-Standard-Dataset"


def clean_name(name: str) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", name).strip("_")
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned


def build_yolo_standard_dataset():
    if not SRC_DIR.exists():
        print(f"Error: {SRC_DIR} does not exist!")
        sys.exit(1)

    for split in ["train", "val", "test"]:
        (DEST_DIR / split).mkdir(parents=True, exist_ok=True)

    crops = sorted([c for c in SRC_DIR.iterdir() if c.is_dir()])
    print(f"Found {len(crops)} crops to merge into YOLO-Standard-Dataset.")

    moved_classes = 0

    for crop in crops:
        crop_clean = clean_name(crop.name)
        classes = sorted([d for d in crop.iterdir() if d.is_dir()])

        for cls_dir in classes:
            cls_clean = clean_name(cls_dir.name)
            if crop_clean.lower() not in cls_clean.lower():
                base_label = f"{crop_clean}_{cls_clean}"
            else:
                base_label = cls_clean

            # Map splits: 'validation' -> 'val', 'train' -> 'train', 'test' -> 'test'
            split_map = {
                "train": "train",
                "validation": "val",
                "test": "test"
            }

            for src_split_name, dest_split_name in split_map.items():
                src_split_dir = cls_dir / src_split_name
                dest_class_dir = DEST_DIR / dest_split_name / base_label

                if src_split_dir.exists():
                    # Move the entire directory atomically
                    os.replace(src_split_dir, dest_class_dir)

            moved_classes += 1

        # Remove now-empty crop directory
        try:
            crop.rmdir()
        except OSError:
            pass

    print(f"\nSuccessfully moved {moved_classes} classes across all crops into YOLO-Standard-Dataset!")
    
    # Print summary counts
    for split in ["train", "val", "test"]:
        split_path = DEST_DIR / split
        class_count = len([d for d in split_path.iterdir() if d.is_dir()])
        img_count = sum(len(list(d.glob("*.*"))) for d in split_path.iterdir() if d.is_dir())
        print(f"  [{split}] {class_count} classes | {img_count} images")


if __name__ == "__main__":
    build_yolo_standard_dataset()
