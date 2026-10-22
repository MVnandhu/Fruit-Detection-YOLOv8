from pathlib import Path
from ultralytics import YOLO

ROOT = Path.cwd()
project_folder = ROOT / "runs_second"

model = YOLO("yolov8s.pt")

model.train(
    data=str(ROOT / "data.yaml"),
    epochs=36,
    imgsz=640,
    batch=8,
    seed=7003,
    freeze=10,
    project=str(project_folder),
    name="freeze10",
    pretrained=True,
    plots=True
)

print("Second experiment completed.")
