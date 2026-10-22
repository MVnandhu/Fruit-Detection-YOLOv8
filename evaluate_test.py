from pathlib import Path
from ultralytics import YOLO

ROOT = Path.cwd()

model_path = (
    ROOT
    / "runs"
    / "detect"
    / "runs"
    / "detect"
    / "train"
    / "weights"
    / "best.pt"
)

data_path = ROOT / "data.yaml"

model = YOLO(str(model_path))

metrics = model.val(
    data=str(data_path),
    split="test",
    imgsz=640,
    batch=8,
    conf=0.23,
    plots=True,
    project=str(ROOT / "evaluation"),
    name="test_overall"
)

precision = float(metrics.box.mp)
recall = float(metrics.box.mr)
f1 = 0.0 if precision + recall == 0 else (
    2 * precision * recall / (precision + recall)
)

print("\nFINAL TEST RESULTS")
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)
print("mAP@0.5:", float(metrics.box.map50))
print("mAP@0.5:0.95:", float(metrics.box.map))

print("\nPER-CLASS RESULTS")
for index, class_name in enumerate(["apple", "banana", "orange"]):
    print(
        class_name,
        "Precision:", float(metrics.box.p[index]),
        "Recall:", float(metrics.box.r[index]),
        "F1:", (
            0.0
            if metrics.box.p[index] + metrics.box.r[index] == 0
            else 2 * metrics.box.p[index] * metrics.box.r[index]
            / (metrics.box.p[index] + metrics.box.r[index])
        ),
        "mAP@0.5:", float(metrics.box.ap50[index]),
        "mAP@0.5:0.95:", float(metrics.box.ap[index])
    )

print("\nEvaluation files saved in:")
print(ROOT / "evaluation" / "test_overall")
