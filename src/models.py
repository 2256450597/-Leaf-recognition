"""CropDiseasePipeline: 两阶段级联分类推理"""
import os
from ultralytics import YOLO
from src.config import MODEL_PATHS, CROP_KEY_MAP, CROP_LABELS, DISEASE_LABELS


class CropDiseasePipeline:
    def __init__(self, device: str = "cpu"):
        self.device = device
        self.crop_model = None
        self.disease_models = {}
        self._loaded = False

    def load_models(self):
        """加载所有模型权重（建议在 GUI 启动时调用一次）"""
        if self._loaded:
            return

        # Stage 1
        if not os.path.exists(MODEL_PATHS["stage1_crop"]):
            raise FileNotFoundError(f"Stage1 weight not found: {MODEL_PATHS['stage1_crop']}")
        self.crop_model = YOLO(MODEL_PATHS["stage1_crop"])

        # Stage 2
        for crop_key in ["tomato", "corn", "potato"]:
            weight_key = f"stage2_{crop_key}"
            if not os.path.exists(MODEL_PATHS[weight_key]):
                raise FileNotFoundError(f"Stage2 weight not found: {MODEL_PATHS[weight_key]}")
            self.disease_models[crop_key] = YOLO(MODEL_PATHS[weight_key])

        self._loaded = True
        print("All 4 models loaded (17 disease classes supported).")

    def predict(self, image_path: str) -> dict:
        """对单张图片执行两阶段推理，返回作物+病害双层结果"""
        if not self._loaded:
            self.load_models()

        # Stage 1: 作物分类
        result1 = self.crop_model(image_path, verbose=False)
        crop_idx = result1[0].probs.top1
        crop_conf = float(result1[0].probs.top1conf)
        crop_key = CROP_KEY_MAP[crop_idx]

        # Stage 2: 病害分类（路由到对应作物模型）
        disease_model = self.disease_models[crop_key]
        result2 = disease_model(image_path, verbose=False)
        disease_idx = result2[0].probs.top1
        disease_conf = float(result2[0].probs.top1conf)

        # 病害索引 → 标签名（YOLO 按字母顺序分配）
        if crop_key == "tomato":
            disease_map = {
                0: "bacterial_spot", 1: "early_blight", 2: "healthy", 3: "late_blight",
                4: "leaf_mold", 5: "septoria_leaf_spot", 6: "spider_mites",
                7: "target_spot", 8: "tomato_mosaic_virus", 9: "tomato_yellow_leaf_curl_virus",
            }
        elif crop_key == "corn":
            disease_map = {0: "common_rust", 1: "gray_leaf_spot", 2: "healthy", 3: "northern_leaf_blight"}
        else:
            disease_map = {0: "early_blight", 1: "healthy", 2: "late_blight"}
        disease_key = disease_map[disease_idx]

        return {
            "crop": CROP_LABELS[crop_key],
            "crop_key": crop_key,
            "disease": DISEASE_LABELS[disease_key],
            "disease_key": disease_key,
            "crop_conf": crop_conf,
            "disease_conf": disease_conf,
        }

    def predict_batch(self, image_paths: list[str]) -> list[dict]:
        """批量推理，返回结果列表"""
        results = []
        for path in image_paths:
            try:
                result = self.predict(path)
                result["file"] = os.path.basename(path)
                result["error"] = None
            except Exception as e:
                result = {
                    "file": os.path.basename(path),
                    "crop": None, "disease": None,
                    "crop_conf": 0, "disease_conf": 0,
                    "error": str(e),
                }
            results.append(result)
        return results
