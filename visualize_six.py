from pathlib import Path
from ultralytics import YOLO
from PIL import Image, ImageDraw

ROOT = Path.cwd()

model_path = (
    ROOT / "runs" / "detect" / "runs" / "detect"
    / "train" / "weights" / "best.pt"
)

model = YOLO(str(model_path))

image_folder = ROOT / "test_own" / "images"
label_folder = ROOT / "test_own" / "labels"
output_folder = ROOT / "six_visualizations"
output_folder.mkdir(exist_ok=True)

class_names = ["apple", "banana", "orange"]
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

images = sorted(
    p for p in image_folder.iterdir()
    if p.suffix.lower() in image_extensions
)[:6]

if len(images) < 6:
    raise RuntimeError("Fewer than six own images were found.")

for image_path in images:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Ground truth boxes: GREEN
    label_path = label_folder / f"{image_path.stem}.txt"

    for line in label_path.read_text().splitlines():
        if not line.strip():
            continue

        parts = line.split()

        if len(parts) != 5:
            continue

        class_id, xc, yc, box_width, box_height = map(float, parts)

        x1 = (xc - box_width / 2) * width
        y1 = (yc - box_height / 2) * height
        x2 = (xc + box_width / 2) * width
        y2 = (yc + box_height / 2) * height

        class_name = class_names[int(class_id)]

        draw.rectangle(
            [x1, y1, x2, y2],
            outline="lime",
            width=4
        )

        draw.text(
            [x1, max(0, y1 - 20)],
            f"GT: {class_name}",
            fill="lime"
        )

    # Predictions: RED
    result = model.predict(
        source=str(image_path),
        imgsz=640,
        conf=0.23,
        verbose=False
    )[0]

    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = class_names[class_id]

        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=4
        )

        draw.text(
            [x1, min(height - 20, y2 + 3)],
            f"P: {class_name} {confidence:.2f}",
            fill="red"
        )

    output_path = output_folder / image_path.name
    image.save(output_path)
    print("Saved:", output_path)

print("Six visualization images created.")
