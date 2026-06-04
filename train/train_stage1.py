"""Stage 1: 作物分类训练（tomato / corn / potato）"""
from ultralytics import YOLO
import os
import shutil


def train_stage1():
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "stage1_crop")

    model = YOLO("yolov8n-cls.pt")

    results = model.train(
        data=DATA_DIR,
        epochs=50,
        imgsz=224,
        batch=32,
        lr0=1e-3,
        optimizer="AdamW",
        device="mps",  # Mac M-series GPU; 无 GPU 则改为 "cpu"
        project="logs",
        name="stage1_crop",
        exist_ok=True,
        # 数据增强
        fliplr=0.5,
        flipud=0.0,
        degrees=15,
    )

    # 保存最佳权重到 weights/
    weights_dir = os.path.join(os.path.dirname(DATA_DIR), "..", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    best_src = os.path.join("runs", "classify", "logs", "stage1_crop", "weights", "best.pt")
    shutil.copy2(best_src, os.path.join(weights_dir, "stage1_crop.pt"))
    print("Stage 1 training done. Best weight saved to weights/stage1_crop.pt")
    return results


if __name__ == "__main__":
    train_stage1()
