# Fruit Detection Using YOLOv8

This project detects three fruit classes:

- Apple
- Banana
- Orange

## Model

- Model: YOLOv8s
- Epochs: 36
- Image size: 640
- Batch size: 8
- Confidence threshold: 0.23

## Results

| Test Set | Precision | Recall | F1 | mAP@0.5 |
|---|---:|---:|---:|---:|
| Roboflow test | 1.000 | 1.000 | 1.000 | 0.995 |
| Personal photos | 0.598 | 0.483 | 0.535 | 0.402 |

## Features

- YOLO-format dataset preparation
- Bounding-box annotation
- YOLOv8 model training
- Model evaluation
- Confusion-matrix analysis
- Prediction visualization

The model performed best on apples and had the most difficulty detecting bananas in crowded scenes.
