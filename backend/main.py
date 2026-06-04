"""FastAPI Backend - 农作物病害检测 API"""
import os
import sys
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import CropDiseasePipeline
from src.export import export_csv

# 生产模式：serve 前端构建产物
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

app = FastAPI(title="CropGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = CropDiseasePipeline()
history: list[dict] = []


@app.on_event("startup")
async def startup():
    pipeline.load_models()
    print("[API] All 4 models loaded.")


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """单张图片推理"""
    import tempfile
    content = await file.read()
    suffix = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = pipeline.predict(tmp_path)
    finally:
        os.unlink(tmp_path)

    result["file"] = file.filename
    result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, result)
    return result


@app.post("/api/batch")
async def batch(files: list[UploadFile] = File(...)):
    """批量图片推理"""
    import tempfile
    results = []
    for file in files:
        content = await file.read()
        suffix = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            result = pipeline.predict(tmp_path)
        finally:
            os.unlink(tmp_path)
        result["file"] = file.filename
        result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append(result)

    history[:0] = results
    return {"total": len(results), "results": results}


@app.get("/api/history")
async def get_history(limit: int = 50):
    """获取历史记录"""
    return history[:limit]


@app.get("/api/export")
async def export():
    """导出 CSV"""
    if not history:
        raise HTTPException(400, "No history to export")
    path = export_csv(history)
    return FileResponse(path, filename="results.csv", media_type="text/csv")


@app.get("/api/health")
async def health():
    return {"status": "ok", "models_loaded": pipeline._loaded}


# 生产模式：静态文件 + SPA 回退
if os.path.exists(FRONTEND_DIST):
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(FRONTEND_DIST, full_path) if full_path else None
        if file_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
