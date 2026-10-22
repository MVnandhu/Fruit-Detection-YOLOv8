from pathlib import Path
from collections import Counter

ROOT = Path.cwd()
class_names = ["apple", "banana", "orange"]
splits = ["train", "valid", "test"]

counts = {}

for split in splits:
    label_folder = ROOT / split / "labels"
    counter = Counter()

    for label_file in label_folder.glob("*.txt"):
        for line in label_file.read_text().splitlines():
            if line.strip():
                class_id = int(line.split()[0])
                counter[class_id] += 1

    counts[split] = [
        counter[0],
        counter[1],
        counter[2]
    ]

    print(split, counts[split])

# Create a simple SVG bar chart without Matplotlib
width = 900
height = 600
left = 100
bottom = 500
chart_width = 700
chart_height = 380

maximum = max(max(values) for values in counts.values())
if maximum == 0:
    maximum = 1

colors = {
    "train": "#4285F4",
    "valid": "#34A853",
    "test": "#FBBC05"
}

svg = []
svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}">'
)
svg.append('<rect width="100%" height="100%" fill="white"/>')
svg.append(
    '<text x="450" y="45" text-anchor="middle" '
    'font-size="26" font-family="Arial">'
    'Class Distribution by Dataset Split</text>'
)

# Axes
svg.append(
    f'<line x1="{left}" y1="{bottom}" '
    f'x2="{left + chart_width}" y2="{bottom}" stroke="black"/>'
)
svg.append(
    f'<line x1="{left}" y1="{bottom}" '
    f'x2="{left}" y2="{bottom - chart_height}" stroke="black"/>'
)

# Y-axis labels
for i in range(6):
    value = int(maximum * i / 5)
    y = bottom - (chart_height * i / 5)

    svg.append(
        f'<text x="{left - 15}" y="{y + 5}" '
        f'text-anchor="end" font-size="14" font-family="Arial">'
        f'{value}</text>'
    )

# Bars
group_width = chart_width / len(class_names)
bar_width = group_width / 4

for class_index, class_name in enumerate(class_names):
    group_x = left + class_index * group_width

    svg.append(
        f'<text x="{group_x + group_width / 2}" y="{bottom + 35}" '
        f'text-anchor="middle" font-size="16" font-family="Arial">'
        f'{class_name}</text>'
    )

    for split_index, split in enumerate(splits):
        value = counts[split][class_index]
        bar_height = (value / maximum) * chart_height
        x = group_x + 25 + split_index * bar_width
        y = bottom - bar_height

        svg.append(
            f'<rect x="{x}" y="{y}" width="{bar_width - 5}" '
            f'height="{bar_height}" fill="{colors[split]}"/>'
        )

        svg.append(
            f'<text x="{x + (bar_width - 5) / 2}" y="{y - 8}" '
            f'text-anchor="middle" font-size="12" font-family="Arial">'
            f'{value}</text>'
        )

# Legend
legend_x = 650
legend_y = 90

for index, split in enumerate(splits):
    y = legend_y + index * 30

    svg.append(
        f'<rect x="{legend_x}" y="{y}" width="18" height="18" '
        f'fill="{colors[split]}"/>'
    )
    svg.append(
        f'<text x="{legend_x + 28}" y="{y + 14}" '
        f'font-size="15" font-family="Arial">{split}</text>'
    )

svg.append('</svg>')

output_file = ROOT / "class_distribution.svg"
output_file.write_text("\n".join(svg), encoding="utf-8")

print("Saved: class_distribution.svg")
