"""推理管线：批量处理与结果汇总"""
import os
import time
from src.models import CropDiseasePipeline


class Pipeline:
    def __init__(self, device: str = "cpu"):
        self.pipeline = CropDiseasePipeline(device=device)

    def run_folder(self, folder_path: str) -> list[dict]:
        """对文件夹内所有图片执行两阶段推理"""
        self.pipeline.load_models()

        exts = {'.jpg', '.jpeg', '.png', '.bmp'}
        image_paths = [
            os.path.join(folder_path, f)
            for f in sorted(os.listdir(folder_path))
            if os.path.splitext(f)[1].lower() in exts
        ]
        if not image_paths:
            print(f"No images found in {folder_path}")
            return []

        print(f"Processing {len(image_paths)} images...")
        start = time.time()
        results = self.pipeline.predict_batch(image_paths)
        elapsed = time.time() - start
        print(f"Done in {elapsed:.2f}s ({len(image_paths) / elapsed:.1f} img/s)")

        # 打印汇总
        diseased = [r for r in results if r["disease"] and r["disease"] != "健康"]
        print(f"  Total: {len(results)}, Healthy: {len(results) - len(diseased)}, Diseased: {len(diseased)}")
        return results

    def run_single(self, image_path: str) -> dict:
        """单张图片推理"""
        self.pipeline.load_models()
        return self.pipeline.predict(image_path)
