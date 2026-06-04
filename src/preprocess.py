"""推理用图像预处理"""
import cv2
import numpy as np
from src.config import INPUT_SIZE, MEAN, STD


def preprocess_image(image_path: str) -> np.ndarray:
    """加载并预处理单张图片，返回归一化的 (3, 224, 224) numpy 数组"""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))
    img = img.astype(np.float32) / 255.0
    img = (img - np.array(MEAN)) / np.array(STD)
    img = np.transpose(img, (2, 0, 1))  # HWC → CHW
    return img


def preprocess_batch(image_paths: list[str]) -> np.ndarray:
    """批量预处理，返回 (N, 3, 224, 224) numpy 数组"""
    batch = [preprocess_image(p) for p in image_paths]
    return np.stack(batch, axis=0)
