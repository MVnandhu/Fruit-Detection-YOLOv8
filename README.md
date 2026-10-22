# Fruit Detection Using YOLOv8

This project uses YOLOv8s to detect three types of fruit:

- Apple
- Banana
- Orange

## Project Overview

The project includes dataset preparation, bounding-box annotation, YOLO-format label validation, model training, evaluation, confusion-matrix analysis, and prediction visualization.

## Model Configuration

- Model: YOLOv8s
- Epochs: 36
- Image size: 640 × 640
- Batch size: 8
- Random seed: 7003
- Confidence threshold: 0.23
- Training framework: Ultralytics YOLO

## Experiments

Two experiments were performed:

1. Standard YOLOv8s training
2. YOLOv8s training with the first 10 layers frozen

Both experiments produced almost identical validation results.

## Results

| Test Set | Images | Precision | Recall | F1-score | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|---:|---:|
| Roboflow test | 3 | 1.000 | 1.000 | 1.000 | 0.995 | 0.962 |
| Personal photographs | 40 | 0.598 | 0.483 | 0.535 | 0.402 | 0.177 |

The Roboflow test set contained only three images, so its results should be interpreted cautiously. The personal-photo evaluation is more informative because it contains 40 images and 150 annotated objects.

## Class-wise Results on Personal Photographs

| Class | Precision | Recall | F1-score | mAP@0.5 |
|---|---:|---:|---:|---:|
| Apple | 0.892 | 0.786 | 0.834 | 0.770 |
| Banana | 0.322 | 0.196 | 0.244 | 0.087 |
| Orange | 0.580 | 0.468 | 0.516 | 0.350 |

Apple was detected most successfully. Banana was the most difficult class because of overlapping objects, different shapes, and missed detections.

## Main Features

- YOLO-format dataset preparation
- Bounding-box annotation
- Label validation
- YOLOv8 model training
- Frozen-layer comparison
- Precision, recall, F1-score, and mAP evaluation
- Confusion-matrix analysis
- Ground-truth and prediction visualization

## Project Structure

```text
Fruit-Detection-YOLOv8/
├── README.md
├── Experiment5_7003.ipynb
├── Fruit_Detection_YOLOv8_Report.pdf
├── train_main.py
├── train_second.py
├── evaluate_test.py
├── evaluate_separate.py
├── visualize_six.py
├── data.yaml
├── data_own.yaml
├── data_robo.yaml
├── figures/
└── six_visualizations/
