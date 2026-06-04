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
    "tomato":  [
        "bacterial_spot", "early_blight", "healthy", "late_blight",
        "leaf_mold", "septoria_leaf_spot", "spider_mites",
        "target_spot", "tomato_mosaic_virus", "tomato_yellow_leaf_curl_virus",
    ],
    "corn":    ["common_rust", "gray_leaf_spot", "healthy", "northern_leaf_blight"],
    "potato":  ["early_blight", "healthy", "late_blight"],
}

DISEASE_LABELS = {
    "healthy":              "健康",
    "bacterial_spot":       "细菌性斑点病",
    "early_blight":         "早疫病",
    "late_blight":          "晚疫病",
    "leaf_mold":            "叶霉病",
    "septoria_leaf_spot":   "斑枯病",
    "spider_mites":         "红蜘蛛",
    "target_spot":          "靶斑病",
    "tomato_mosaic_virus":  "花叶病毒病",
    "tomato_yellow_leaf_curl_virus": "黄化曲叶病毒病",
    "common_rust":          "普通锈病",
    "gray_leaf_spot":       "灰斑病",
    "northern_leaf_blight": "北方叶枯病",
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
