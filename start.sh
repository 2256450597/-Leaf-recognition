#!/bin/bash
# CropGuard Startup Script
# 使用方法: bash start.sh [dev|prod]

MODE=${1:-prod}
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
SSL_CERT_FILE=/tmp/crop_disease_env/env/ssl/cert.pem

echo "========================================="
echo "  CropGuard - 农作物病害检测分析平台"
echo "========================================="

if [ "$MODE" = "dev" ]; then
    echo "[Dev Mode] 启动前端开发服务器 + 后端 API"
    echo ""
    echo "  前端: http://localhost:5173"
    echo "  后端: http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
    echo ""

    # Start backend
    export SSL_CERT_FILE
    /tmp/crop_disease_env/env/bin/python "$PROJECT_DIR/backend/main.py" &
    BACKEND_PID=$!

    # Start frontend dev server
    cd "$PROJECT_DIR/frontend"
    npm run dev &
    FRONTEND_PID=$!

    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    wait

else
    echo "[Prod Mode] 访问 http://localhost:8000"
    echo "  API文档: http://localhost:8000/docs"
    echo ""

    # Build frontend if needed
    if [ ! -d "$PROJECT_DIR/frontend/dist" ]; then
        echo "[Build] Building frontend..."
        cd "$PROJECT_DIR/frontend" && npm run build
    fi

    # Start backend (serves frontend + API)
    cd "$PROJECT_DIR"
    export SSL_CERT_FILE
    /tmp/crop_disease_env/env/bin/python "$PROJECT_DIR/backend/main.py"
fi
