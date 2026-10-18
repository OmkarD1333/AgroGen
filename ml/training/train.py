from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = ROOT / "ml" / "disease_detection" / "YOLO-Standard-Dataset"

# Point to your best checkpoint from the completed 10-epoch run
CHECKPOINT = (
    ROOT
    / "ml"
    / "disease_detection"
    / "weights"
    / "yolov8_disease-5"
    / "weights"
    / "best.pt"  # or last.pt
)


def main():
    if CHECKPOINT.exists():
        print(f"🔄 Loading weights from: {CHECKPOINT}")
        # Initialize the model with your checkpoint weights
        model = YOLO(str(CHECKPOINT))
    else:
        print("🚀 Checkpoint not found. Starting fresh training...")
        model = YOLO("yolov8n-cls.pt")

    # Run 15 additional epochs
    model.train(
        data=str(DATA_PATH),
        epochs=15,          # 15 additional epochs
        imgsz=224,
        batch=32,
        device=0,
        workers=4,
        project=str(ROOT / "ml" / "disease_detection" / "weights"),
        name="yolov8_disease",
    )


if __name__ == "__main__":
    main()
