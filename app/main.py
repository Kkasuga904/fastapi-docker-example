from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="FastAPI Production Example",
    description="Production-ready FastAPI application with monitoring and scalability",
    version="1.0.0"
)

# CORS設定（本番環境では適切に設定する）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ヘルスチェックエンドポイント（K8s liveness probe用）
@app.get("/health")
def health_check():
    """
    Kubernetes liveness/readiness probe endpoint
    Returns OK if the service is healthy
    """
    return {"status": "healthy", "service": "fastapi-app"}

# ルートエンドポイント
@app.get("/")
def root():
    """
    Welcome endpoint
    Returns basic API information
    """
    return {
        "message": "Welcome to FastAPI Production Example",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

# サンプルAPI（名前付き挨拶）
@app.get("/hello/{name}")
def hello_name(name: str):
    """
    Personalized greeting endpoint
    Args:
        name: Name to greet
    Returns:
        Personalized greeting message
    """
    return {"message": f"Hello, {name}!"}

# メトリクス用エンドポイント（Prometheus用）
@app.get("/metrics")
def metrics():
    """
    Prometheus metrics endpoint
    Returns basic application metrics
    """
    return {
        "requests_total": 1000,
        "requests_per_second": 10,
        "response_time_ms": 50,
        "active_connections": 5
    }