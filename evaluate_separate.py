from pathlib import Path
from ultralytics import YOLO

ROOT = Path.cwd()

model_path = (
    ROOT / "runs" / "detect" / "runs" / "detect"
    / "train" / "weights" / "best.pt"
)

model = YOLO(str(model_path))

for name, yaml_file in [
    ("roboflow_test", "data_robo.yaml"),
    ("own_test", "data_own.yaml"),
]:
    print(f"\n===== {name} =====")

    metrics = model.val(
        data=str(ROOT / yaml_file),
        split="test",
        imgsz=640,
        batch=8,
        conf=0.23,
        plots=True,
        project=str(ROOT / "evaluation_separate"),
        name=name,
    )

    precision = float(metrics.box.mp)
    recall = float(metrics.box.mr)

    f1 = (
        0.0
        if precision + recall == 0
        else 2 * precision * recall / (precision + recall)
    )

    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)
    print("mAP@0.5:", float(metrics.box.map50))
    print("mAP@0.5:0.95:", float(metrics.box.map))
