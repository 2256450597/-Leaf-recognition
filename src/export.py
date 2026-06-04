"""结果导出：CSV 格式"""
import csv
from datetime import datetime

CSV_COLUMNS = ["文件名", "作物", "病害", "作物置信度", "病害置信度", "错误信息"]


def export_csv(results: list[dict], output_path: str = None) -> str:
    """将推理结果列表导出为 CSV，返回文件路径"""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"results_{timestamp}.csv"

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        for r in results:
            writer.writerow([
                r.get("file", ""),
                r.get("crop", ""),
                r.get("disease", ""),
                f"{r.get('crop_conf', 0):.2%}",
                f"{r.get('disease_conf', 0):.2%}",
                r.get("error", ""),
            ])

    print(f"Results exported to {output_path} ({len(results)} rows)")
    return output_path
