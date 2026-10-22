from ultralytics import YOLO

model = YOLO("yolov8s.pt")

results = model.train(
    data="data.yaml",
    epochs=36,
    imgsz=640,
    batch=8,
    seed=7003,
    project="runs/detect",
    name="train",
    pretrained=True,
    plots=True
)

print("Main training completed.")
