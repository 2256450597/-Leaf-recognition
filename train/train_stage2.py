"""Stage 2: 病害分类训练 — 番茄 / 玉米 / 马铃薯各一个模型"""
from ultralytics import YOLO
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_ROOT = os.path.join(ROOT, "data")
WEIGHTS_DIR = os.path.join(ROOT, "weights")
os.makedirs(WEIGHTS_DIR, exist_ok=True)

STAGE2_CONFIG = [
    {"name": "stage2_tomato", "data": os.path.join(DATA_ROOT, "stage2_tomato")},
    {"name": "stage2_corn",   "data": os.path.join(DATA_ROOT, "stage2_corn")},
    {"name": "stage2_potato", "data": os.path.join(DATA_ROOT, "stage2_potato")},
]


def train_one(config):
    model = YOLO("yolov8n-cls.pt")
    results = model.train(
        data=config["data"],
        epochs=50,
        imgsz=224,
        batch=32,
        lr0=1e-3,
        optimizer="AdamW",
        device="mps",
        project="logs",
        name=config["name"],
        exist_ok=True,
        fliplr=0.5,
        flipud=0.0,
        degrees=15,
    )
    best_src = os.path.join("runs", "classify", "logs", config["name"], "weights", "best.pt")
    shutil.copy2(best_src, os.path.join(WEIGHTS_DIR, f"{config['name']}.pt"))
    print(f"{config['name']} done. Best weight saved.")
    return results


def train_all():
    for cfg in STAGE2_CONFIG:
        print(f"\n=== Training {cfg['name']} ===")
        train_one(cfg)


if __name__ == "__main__":
    train_all()
