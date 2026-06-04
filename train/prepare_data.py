"""PlantVillage 数据重组：拆分为 Stage1 + Stage2 目录结构"""
import os
import shutil
from sklearn.model_selection import train_test_split

# ===== 配置（按实际路径修改）=====
PLANTVILLAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PlantVillage_raw")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
VAL_RATIO = 0.2
RANDOM_SEED = 42

# 要处理的作物及其病害映射
CROP_MAP = {
    "tomato":  [
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___healthy",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    ],
    "corn":    [
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Corn_(maize)___healthy",
        "Corn_(maize)___Northern_Leaf_Blight",
    ],
    "potato":  [
        "Potato___Bacteria",
        "Potato___Early_blight",
        "Potato___Fungi",
        "Potato___healthy",
        "Potato___Late_blight",
        "Potato___Nematode",
        "Potato___Pest",
        "Potato___Phytopthora",
        "Potato___Virus",
    ],
}


def prepare_stage1():
    """Stage 1: 作物分类数据 — 每种作物的全部样本合并到一个目录"""
    stage1_dir = os.path.join(OUTPUT_DIR, "stage1_crop")
    for split in ["train", "val"]:
        for crop in CROP_MAP:
            os.makedirs(os.path.join(stage1_dir, split, crop), exist_ok=True)

    for crop, dirs in CROP_MAP.items():
        for raw_dir in dirs:
            src_dir = os.path.join(PLANTVILLAGE_DIR, raw_dir)
            if not os.path.exists(src_dir):
                print(f"  WARNING: {src_dir} not found, skipping")
                continue
            images = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            train_imgs, val_imgs = train_test_split(images, test_size=VAL_RATIO, random_state=RANDOM_SEED)

            for img in train_imgs:
                shutil.copy2(os.path.join(src_dir, img),
                             os.path.join(stage1_dir, "train", crop, img))
            for img in val_imgs:
                shutil.copy2(os.path.join(src_dir, img),
                             os.path.join(stage1_dir, "val", crop, img))
            print(f"  {raw_dir}: {len(train_imgs)} train, {len(val_imgs)} val")
    print("Stage 1 data ready.")


def prepare_stage2():
    """Stage 2: 病害分类数据 — 每种作物单独组织"""
    for crop, dirs in CROP_MAP.items():
        stage2_dir = os.path.join(OUTPUT_DIR, f"stage2_{crop}")
        if crop == "tomato":
            label_dirs = [
                "bacterial_spot", "early_blight", "healthy", "late_blight",
                "leaf_mold", "septoria_leaf_spot", "spider_mites",
                "target_spot", "tomato_mosaic_virus", "tomato_yellow_leaf_curl_virus",
            ]
        elif crop == "corn":
            label_dirs = ["common_rust", "gray_leaf_spot", "healthy", "northern_leaf_blight"]
        else:
            label_dirs = [
                "bacteria", "early_blight", "fungi", "healthy", "late_blight",
                "nematode", "pest", "phytopthora", "virus",
            ]

        for split in ["train", "val"]:
            for label_dir in label_dirs:
                os.makedirs(os.path.join(stage2_dir, split, label_dir), exist_ok=True)

        for i, raw_dir in enumerate(dirs):
            src_dir = os.path.join(PLANTVILLAGE_DIR, raw_dir)
            if not os.path.exists(src_dir):
                print(f"  WARNING: {src_dir} not found, skipping")
                continue
            label_dir = label_dirs[i]

            images = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            train_imgs, val_imgs = train_test_split(images, test_size=VAL_RATIO, random_state=RANDOM_SEED)
            for img in train_imgs:
                shutil.copy2(os.path.join(src_dir, img), os.path.join(stage2_dir, "train", label_dir, img))
            for img in val_imgs:
                shutil.copy2(os.path.join(src_dir, img), os.path.join(stage2_dir, "val", label_dir, img))
            print(f"  {raw_dir} -> {label_dir}: {len(train_imgs)} train, {len(val_imgs)} val")
        print(f"Stage 2 ({crop}) data ready.")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=== Stage 1: Crop Classification Data ===")
    prepare_stage1()
    print("\n=== Stage 2: Disease Classification Data ===")
    prepare_stage2()
    print("\nDone! Output at:", OUTPUT_DIR)
