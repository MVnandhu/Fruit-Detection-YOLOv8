from pathlib import Path
import base64
import html
import json

ROOT = Path.cwd()
image_folder = ROOT / "test" / "images"
label_folder = ROOT / "test" / "labels"

class_names = ["apple", "banana", "orange"]
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

images = sorted(
    p for p in image_folder.iterdir()
    if p.suffix.lower() in image_extensions
    and p.stem.lower().startswith("photo")
)[:3]

if len(images) < 3:
    raise RuntimeError("Fewer than 3 own photos were found.")

cards = []

for image_path in images:
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")

    if image_path.suffix.lower() in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif image_path.suffix.lower() == ".png":
        mime = "image/png"
    else:
        mime = "image/jpeg"

    boxes = []
    label_path = label_folder / f"{image_path.stem}.txt"

    if label_path.exists():
        for line in label_path.read_text().splitlines():
            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                continue

            class_id, xc, yc, bw, bh = map(float, parts)

            boxes.append({
                "class_name": class_names[int(class_id)],
                "xc": xc,
                "yc": yc,
                "bw": bw,
                "bh": bh
            })

    cards.append({
        "name": image_path.name,
        "src": f"data:{mime};base64,{encoded}",
        "boxes": boxes
    })

data = json.dumps(cards)

html_file = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Three Ground-Truth Examples</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: white;
}}

.container {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}}

.card {{
    width: 31%;
    min-width: 350px;
}}

.title {{
    text-align: center;
    font-weight: bold;
    margin-bottom: 8px;
}}

.viewer {{
    position: relative;
    width: 100%;
}}

.viewer img {{
    display: block;
    width: 100%;
    height: auto;
}}

.overlay {{
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}}

.box {{
    position: absolute;
    border: 3px solid lime;
    box-sizing: border-box;
}}

.box-label {{
    position: absolute;
    left: 0;
    top: -23px;
    color: lime;
    background: rgba(0, 0, 0, 0.7);
    font-size: 15px;
    padding: 2px 4px;
    white-space: nowrap;
}}
</style>
</head>

<body>
<h1>Ground-Truth Boxes for Three Own Photos</h1>
<div class="container" id="container"></div>

<script>
const cards = {data};
const container = document.getElementById("container");

for (const card of cards) {{
    const cardElement = document.createElement("div");
    cardElement.className = "card";

    const title = document.createElement("div");
    title.className = "title";
    title.textContent = card.name;

    const viewer = document.createElement("div");
    viewer.className = "viewer";

    const image = document.createElement("img");
    image.src = card.src;

    const overlay = document.createElement("div");
    overlay.className = "overlay";

    viewer.appendChild(image);
    viewer.appendChild(overlay);
    cardElement.appendChild(title);
    cardElement.appendChild(viewer);
    container.appendChild(cardElement);

    image.onload = function() {{
        for (const box of card.boxes) {{
            const rectangle = document.createElement("div");
            rectangle.className = "box";

            rectangle.style.left = ((box.xc - box.bw / 2) * 100) + "%";
            rectangle.style.top = ((box.yc - box.bh / 2) * 100) + "%";
            rectangle.style.width = (box.bw * 100) + "%";
            rectangle.style.height = (box.bh * 100) + "%";

            const label = document.createElement("div");
            label.className = "box-label";
            label.textContent = box.class_name;

            rectangle.appendChild(label);
            overlay.appendChild(rectangle);
        }}
    }};
}}
</script>
</body>
</html>
"""

output = ROOT / "three_ground_truth_examples.html"
output.write_text(html_file, encoding="utf-8")

print("Selected images:")
for image in images:
    print("-", image.name)

print("Saved: three_ground_truth_examples.html")
