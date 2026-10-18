import argparse
import sys
from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = ROOT / "ml" / "disease_detection" / "weights" / "best.pt"

# Common synonyms for crops
CROP_ALIASES = {
    "eggplant": "brinjal",
    "corn": "maize",
    "pepper": "chilli",
    "chili": "chilli",
}


def load_model():
    if not MODEL_PATH.exists():
        alt_path = ROOT / "ml" / "disease_detection" / "weights" / "yolov8_disease-6" / "weights" / "best.pt"
        if alt_path.exists():
            return YOLO(str(alt_path))
        raise FileNotFoundError(f"Model weights not found at: {MODEL_PATH}")
    return YOLO(str(MODEL_PATH))


def get_available_crops(model: YOLO) -> list[str]:
    crops = set()
    for name in model.names.values():
        name_lower = name.lower()
        if "apple" in name_lower:
            crops.add("apple")
        else:
            crops.add(name_lower.split("_")[0])
    return sorted(list(crops))


def filter_classes_by_crop(model: YOLO, crop: str) -> list[int]:
    clean_crop = crop.strip().lower()
    clean_crop = CROP_ALIASES.get(clean_crop, clean_crop)
    matching_ids = []
    for cls_id, cls_name in model.names.items():
        if clean_crop in cls_name.lower():
            matching_ids.append(cls_id)
    return matching_ids


def predict_image(model: YOLO, img_path: Path, crop: str = None):
    if not img_path.exists():
        print(f"Error: Image file not found: {img_path}")
        return

    print(f"\nAnalyzing image: {img_path.name}...")
    results = model.predict(source=str(img_path), verbose=False)
    result = results[0]
    all_probs = result.probs.data.cpu().numpy()

    # --- Mode 1: Crop-specific filtered prediction ---
    if crop:
        clean_crop = CROP_ALIASES.get(crop.strip().lower(), crop.strip().lower())
        matched_ids = filter_classes_by_crop(model, clean_crop)

        if not matched_ids:
            available = ", ".join(get_available_crops(model))
            print(f"Warning: No classes found for crop '{crop}'.")
            print(f"Available crops: {available}")
            print("Falling back to all classes...\n")
        else:
            # Gather probabilities for matching crop classes
            crop_probs = {cls_id: float(all_probs[cls_id]) for cls_id in matched_ids}
            total_prob = sum(crop_probs.values()) or 1e-9

            # Normalize probabilities to sum to 100% within the chosen crop
            sorted_crop = sorted(crop_probs.items(), key=lambda x: x[1], reverse=True)
            top_id, raw_conf = sorted_crop[0]
            relative_conf = raw_conf / total_prob

            print("\n" + "=" * 50)
            print(f"Crop Filter:    {clean_crop.upper()}")
            print(f"Top Prediction: {model.names[top_id]}")
            print(f"Confidence:     {relative_conf:.2%}")
            print("=" * 50)

            print(f"\nDisease Ranking for {clean_crop.title()}:")
            for rank, (cls_id, c_conf) in enumerate(sorted_crop, start=1):
                name = model.names[cls_id]
                rel = c_conf / total_prob
                bar = "#" * int(rel * 25)
                print(f"  {rank}. {name:<35} {rel:>6.2%} | {bar}")
            print("=" * 50 + "\n")
            return

    # --- Mode 2: Global unconstrained prediction (All 95 classes) ---
    top1_id = result.probs.top1
    top1_name = result.names[top1_id]
    top1_conf = float(result.probs.top1conf)

    print("\n" + "=" * 50)
    print(f"Top Prediction: {top1_name}")
    print(f"Confidence:     {top1_conf:.2%}")
    print("=" * 50)

    print("\nTop 5 Predictions (Global):")
    top5_ids = result.probs.top5
    top5_confs = result.probs.top5conf.tolist()
    for rank, (cls_id, conf) in enumerate(zip(top5_ids, top5_confs), start=1):
        name = result.names[cls_id]
        bar = "#" * int(conf * 25)
        print(f"  {rank}. {name:<35} {conf:>6.2%} | {bar}")
    print("=" * 50 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="AgroGen AI Disease Inference")
    parser.add_argument("image", nargs="?", help="Path to leaf image")
    parser.add_argument("--crop", "-c", type=str, default=None, help="Crop filter (e.g. brinjal, potato, apple)")
    return parser.parse_args()


def main():
    args = parse_args()

    print("Loading model weights...")
    model = load_model()
    print("Model loaded successfully!")

    # 1. If image path is passed as command line argument
    if args.image:
        img_path = Path(args.image.strip('"').strip("'"))
        predict_image(model, img_path, crop=args.crop)
        return

    # 2. Interactive mode: prompt in terminal
    available_crops = ", ".join(get_available_crops(model))
    print("\n[Interactive Mode]")
    print(f"Available Crops: {available_crops}")
    print("Type 'q' or 'exit' at any prompt to quit.\n")

    while True:
        try:
            user_input = input("Enter image path (or drag & drop): ").strip().strip('"').strip("'")
            if not user_input:
                continue
            if user_input.lower() in ("q", "quit", "exit"):
                print("Exiting.")
                break

            img_path = Path(user_input)
            if not img_path.exists():
                print(f"Error: File not found: {img_path}\n")
                continue

            crop_input = input("Enter crop name [Press Enter for all]: ").strip().strip('"').strip("'")
            if crop_input.lower() in ("q", "quit", "exit"):
                print("Exiting.")
                break

            crop_filter = crop_input if crop_input else None
            predict_image(model, img_path, crop=crop_filter)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()