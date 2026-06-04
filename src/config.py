"""全局配置：标签映射、路径常量"""
import os

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Stage 1: 作物分类
CROP_CLASSES = ["tomato", "corn", "potato"]
CROP_LABELS = {
    "tomato": "番茄",
    "corn": "玉米",
    "potato": "马铃薯",
}
CROP_KEY_MAP = {0: "corn", 1: "potato", 2: "tomato"}  # YOLO 按字母顺序：corn, potato, tomato

# Stage 2: 病害分类（按作物分组）
DISEASE_CLASSES = {
    "tomato":  ["healthy", "early_blight", "late_blight"],
    "corn":    ["healthy", "northern_leaf_blight", "common_rust"],
    "potato":  ["healthy", "early_blight", "late_blight"],
}

DISEASE_LABELS = {
    "healthy":              "健康",
    "early_blight":         "早疫病",
    "late_blight":          "晚疫病",
    "northern_leaf_blight": "北方叶枯病",
    "common_rust":          "普通锈病",
}

# 模型权重路径
WEIGHTS_DIR = os.path.join(ROOT_DIR, "weights")
MODEL_PATHS = {
    "stage1_crop":    os.path.join(WEIGHTS_DIR, "stage1_crop.pt"),
    "stage2_tomato":  os.path.join(WEIGHTS_DIR, "stage2_tomato.pt"),
    "stage2_corn":    os.path.join(WEIGHTS_DIR, "stage2_corn.pt"),
    "stage2_potato":  os.path.join(WEIGHTS_DIR, "stage2_potato.pt"),
}

# 图像预处理参数
INPUT_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
