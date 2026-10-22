from pathlib import Path
import shutil

ROOT = Path.cwd()

# Make backups before changing anything
for split in ["train", "valid","test"]:
    label_folder = ROOT / split / "labels"
    backup_folder = ROOT / split / "labels_backup"

    if label_folder.exists() and not backup_folder.exists():
        shutil.copytree(label_folder, backup_folder)
        print(f"Backup created: {backup_folder}")

def polygon_to_box(parts):
    """
    Convert:
        class_id x1 y1 x2 y2 x3 y3 ...
    into:
        class_id center_x center_y width height
    """

    class_id = int(parts[0])
    coordinates = [float(value) for value in parts[1:]]

    if len(coordinates) < 6 or len(coordinates) % 2 != 0:
        raise ValueError("Invalid polygon coordinate count")

    x_values = coordinates[0::2]
    y_values = coordinates[1::2]

    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    if width <= 0 or height <= 0:
        raise ValueError("Polygon has zero width or height")

    return (
        f"{class_id} "
        f"{center_x:.6f} {center_y:.6f} "
        f"{width:.6f} {height:.6f}"
    )

for split in ["train", "valid","test"]:
    label_folder = ROOT / split / "labels"

    for label_file in label_folder.glob("*.txt"):
        output_lines = []

        for line_number, line in enumerate(
            label_file.read_text().splitlines(), start=1
        ):
            if not line.strip():
                continue

            parts = line.split()

            if len(parts) == 5:
                # Already standard YOLO bounding-box format
                output_lines.append(" ".join(parts))
            elif len(parts) > 5:
                # Convert polygon to bounding box
                output_lines.append(polygon_to_box(parts))
            else:
                raise ValueError(
                    f"{label_file.name}, line {line_number}: "
                    f"not enough values"
                )

        label_file.write_text(
            "\n".join(output_lines) +
            ("\n" if output_lines else "")
        )

    print(f"Converted labels in: {split}/labels")

print("Conversion complete.")
print("Backups are stored in train/labels_backup and valid/labels_backup.")
