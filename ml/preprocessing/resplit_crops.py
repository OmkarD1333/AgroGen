"""
Re-split chilli, wheat, and rice datasets into proper 70/15/15 ratio.

For each crop:
1. Collects ALL images from the original dataset folder (merging train/test/valid splits)
2. Shuffles with a fixed random seed for reproducibility
3. Splits into 70% train / 15% test / 15% validation
4. Clears the existing dataset_split folders and writes the new split
"""

import os
import shutil
import random
import math
from pathlib import Path

# Fixed seed for reproducibility
RANDOM_SEED = 42
TRAIN_RATIO = 0.70
TEST_RATIO = 0.15
VAL_RATIO = 0.15

BASE_DIR = Path(r"c:\Users\Piyush\OneDrive\Desktop\AgroGen\ml\disease_detection")
DATASET_DIR = BASE_DIR / "dataset"
SPLIT_DIR = BASE_DIR / "dataset_split"


def collect_all_images(directories: list[Path]) -> list[Path]:
    """Collect all image files from a list of directories (non-recursive per dir)."""
    IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}
    images = []
    for d in directories:
        if not d.exists():
            continue
        for f in d.iterdir():
            if f.is_file() and f.suffix.lower() in IMAGE_EXTS:
                images.append(f)
    return images


def split_and_copy(images: list[Path], dest_class_dir: Path, class_name: str):
    """Shuffle images and copy into train/test/validation under dest_class_dir."""
    random.shuffle(images)
    total = len(images)
    
    n_train = math.floor(total * TRAIN_RATIO)
    n_test = math.floor(total * TEST_RATIO)
    n_val = total - n_train - n_test  # remainder goes to validation

    splits = {
        "train": images[:n_train],
        "test": images[n_train:n_train + n_test],
        "validation": images[n_train + n_test:],
    }

    for split_name, split_images in splits.items():
        split_dir = dest_class_dir / split_name
        # Clear existing
        if split_dir.exists():
            shutil.rmtree(split_dir)
        split_dir.mkdir(parents=True, exist_ok=True)

        for img in split_images:
            shutil.copy2(img, split_dir / img.name)

    train_pct = round(n_train / total * 100, 1) if total > 0 else 0
    test_pct = round(n_test / total * 100, 1) if total > 0 else 0
    val_pct = round(n_val / total * 100, 1) if total > 0 else 0
    print(f"  {class_name}: {total} total -> Train: {n_train} ({train_pct}%) | "
          f"Test: {n_test} ({test_pct}%) | Val: {n_val} ({val_pct}%)")


def resplit_wheat():
    """Re-split wheat from original dataset/crop/wheat/data (train+test+valid merged)."""
    print("\n" + "=" * 60)
    print("WHEAT - Re-splitting to 70/15/15")
    print("=" * 60)

    orig_base = DATASET_DIR / "crop" / "wheat" / "data"
    dest_base = SPLIT_DIR / "wheat"

    # Mapping: dataset_split class name -> original folder names across splits
    # Original train has: Aphid, Black Rust, Blast, etc.
    # Original test has: aphid_test, black_rust_test, etc.
    # Original valid has: aphid_valid, black_rust_valid, etc.
    class_mapping = {
        "aphid":                 ("Aphid",                "aphid_test",                  "aphid_valid"),
        "Black Rust":            ("Black Rust",           "black_rust_test",             "black_rust_valid"),
        "blast":                 ("Blast",                "blast_test",                  "blast_test_valid"),
        "Brown Rust":            ("Brown Rust",           "brown_rust_test",             "brown_rust_valid"),
        "Common Root Rot":       ("Common Root Rot",      "common_root_rot_test",        "common_root_rot_valid"),
        "Fusarium Head Blight":  ("Fusarium Head Blight", "fusarium_head_blight_test",   "fusarium_head_blight_valid"),
        "healthy":               ("Healthy",              "healthy_test",                "healthy_valid"),
        "Leaf Blight":           ("Leaf Blight",          "leaf_blight_test",            "leaf_blight_valid"),
        "mildew":                ("Mildew",               "mildew_test",                 "mildew_valid"),
        "mite":                  ("Mite",                 "mite_test",                   "mite_valid"),
        "septoria":              ("Septoria",             "septoria_test",               "septoria_valid"),
        "smut":                  ("Smut",                 "smut_test",                   "smut_valid"),
        "Stem fly":              ("Stem fly",             "stem_fly_test",               "stem_fly_valid"),
        "Tan spot":              ("Tan spot",             "tan_spot_test",               "tan_spot_valid"),
        "Yellow Rust":           ("Yellow Rust",          "yellow_rust_test",            "yellow_rust_valid"),
    }

    random.seed(RANDOM_SEED)

    for split_class_name, (train_folder, test_folder, valid_folder) in class_mapping.items():
        source_dirs = [
            orig_base / "train" / train_folder,
            orig_base / "test" / test_folder,
            orig_base / "valid" / valid_folder,
        ]
        images = collect_all_images(source_dirs)
        if not images:
            print(f"  WARNING: No images found for {split_class_name}")
            continue

        dest_class_dir = dest_base / split_class_name
        split_and_copy(images, dest_class_dir, split_class_name)


def resplit_chilli():
    """Re-split chilli from original dataset/vegetable/chilli dataset (train+test merged)."""
    print("\n" + "=" * 60)
    print("CHILLI - Re-splitting to 70/15/15")
    print("=" * 60)

    orig_base = DATASET_DIR / "vegetable" / "chilli dataset" / "cropped_resized" / "resized_cropped_chilly"
    dest_base = SPLIT_DIR / "chilli"

    # Chilli original only has train and test (no validation)
    # Class names are the same across splits
    classes = ["cercospora", "healthy", "mites_and_trips", "nutritional", "powdery mildew"]

    random.seed(RANDOM_SEED)

    for cls in classes:
        source_dirs = [
            orig_base / "train" / cls,
            orig_base / "test" / cls,
        ]
        images = collect_all_images(source_dirs)
        if not images:
            print(f"  WARNING: No images found for {cls}")
            continue

        dest_class_dir = dest_base / cls
        split_and_copy(images, dest_class_dir, cls)


def resplit_rice():
    """Re-split rice from original dataset/crop/Rice dataset.
    
    Sources:
    - Rice leaf augumention/ (flat folders per disease, no split)
    - Rice disease leaf/ (Train + Test split)
    
    All are merged and re-split to 70/15/15.
    """
    print("\n" + "=" * 60)
    print("RICE - Re-splitting to 70/15/15")
    print("=" * 60)

    orig_base = DATASET_DIR / "crop" / "Rice dataset"
    aug_base = orig_base / "Rice leaf augumention"
    disease_base = orig_base / "Rice disease leaf"
    dest_base = SPLIT_DIR / "rice"

    # Mapping: dataset_split class name -> (augmentation folder, disease_leaf train folder, disease_leaf test folder)
    class_mapping = {
        "bacterial leaf blight":  ("Bacterial Leaf Blight",     "bacterial_leaf_blight",  "bacterial leaf blight"),
        "brown spot":             ("Brown Spot",                "brown_spot",             "brown spot"),
        "healthy":                ("Healthy Rice Leaf",         "healthy",                "healthy"),
        "leaf blast":             ("Leaf Blast",                "leaf_blast",             "leaf blast"),
        "leaf scald":             ("Leaf scald",                "leaf_scald",             "leaf scald"),
        "Narrow Brown Leaf Spot": ("Narrow Brown Leaf Spot",    "narrow_brown_spot",      "narrow brown spot"),
        "Neck_Blast":             ("Neck_Blast",                "neck_blast",             "Neck_Blast"),
        "Rice Hispa":             ("Rice Hispa",                "rice_hispa",             "Rice Hispa"),
        "Sheath Blight":          ("Sheath Blight",             "sheath_blight",          "Sheath Blight"),
        "tungro":                 ("Tungro",                    "tungro",                 "tungro"),
    }

    random.seed(RANDOM_SEED)

    for split_class_name, (aug_folder, train_folder, test_folder) in class_mapping.items():
        source_dirs = [
            aug_base / aug_folder,
            disease_base / "Train" / train_folder,
            disease_base / "Test" / test_folder,
        ]
        images = collect_all_images(source_dirs)
        if not images:
            print(f"  WARNING: No images found for {split_class_name}")
            continue

        # Deduplicate by filename (same image may appear in both augmentation and disease leaf)
        seen = {}
        unique_images = []
        for img in images:
            if img.name not in seen:
                seen[img.name] = img
                unique_images.append(img)
        
        if len(unique_images) < len(images):
            print(f"  Note: {split_class_name} - removed {len(images) - len(unique_images)} duplicates "
                  f"({len(images)} -> {len(unique_images)})")
            images = unique_images

        dest_class_dir = dest_base / split_class_name
        split_and_copy(images, dest_class_dir, split_class_name)


if __name__ == "__main__":
    print("Dataset Re-Split Script")
    print(f"Ratios: Train={TRAIN_RATIO} | Test={TEST_RATIO} | Val={VAL_RATIO}")
    print(f"Random Seed: {RANDOM_SEED}")
    
    resplit_chilli()
    resplit_wheat()
    resplit_rice()
    
    print("\n" + "=" * 60)
    print("DONE! All three crops have been re-split to 70/15/15.")
    print("=" * 60)
