# Security configuration for FastAPI application
# Author: Kkasuga904
# Description: Production security settings and middleware

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import os

def setup_security(app: FastAPI):
    """
    Configure security middleware and settings for production
    """
    
    # ===========================
    # Security Headers
    # ===========================
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        # セキュリティヘッダーの追加
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        # サーバー情報の隠蔽
        response.headers["Server"] = "FastAPI"
        return response
    
    # ===========================
    # Rate Limiting Configuration
    # ===========================
    # Note: In production, use Redis-based rate limiting
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100 per minute"]
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # ===========================
    # Trusted Host Middleware
    # ===========================
    # 本番環境では実際のドメインに変更
    if os.getenv("ENVIRONMENT") == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.example.com", "example.com"]
        )
    
    # ===========================
    # Compression Middleware
    # ===========================
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # ===========================
    # Session Middleware
    # ===========================
    secret_key = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        https_only=True,  # HTTPS環境でのみCookieを送信
        same_site="strict"  # CSRF攻撃防止
    )
    
    return app

# ===========================
# Environment Variables Validation
# ===========================
def validate_environment():
    """
    Validate required environment variables for security
    """
    required_vars = [
        "SECRET_KEY",
        "DATABASE_URL",
        "JWT_SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        # 開発環境では警告、本番環境ではエラー
        if os.getenv("ENVIRONMENT") == "production":
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        else:
            print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")

# ===========================
# Input Validation Schemas
# ===========================
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class SecureInputModel(BaseModel):
    """Base model with security validations"""
    
    class Config:
        # SQLインジェクション対策
        anystr_strip_whitespace = True
        max_anystr_length = 1024
    
    @validator('*', pre=True)
    def prevent_sql_injection(cls, v):
        if isinstance(v, str):
            # 危険な文字列パターンをチェック
            dangerous_patterns = [
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|CREATE|ALTER)\b)",
                r"(--|;|\/\*|\*\/|xp_|sp_|0x)"
            ]
            for pattern in dangerous_patterns:
                if re.search(pattern, v, re.IGNORECASE):
                    raise ValueError("Potentially dangerous input detected")
        return v

# ===========================
# API Key Authentication
# ===========================
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import hashlib

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key for protected endpoints
    """
    if not api_key:
        raise HTTPException(status_code=403, detail="API key required")
    
    # ハッシュ化して比較（タイミング攻撃対策）
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    valid_key_hash = hashlib.sha256(
        os.getenv("API_KEY", "").encode()
    ).hexdigest()
    
    if not secrets.compare_digest(api_key_hash, valid_key_hash):
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return api_key