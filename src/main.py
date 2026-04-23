from fastapi import FastAPI
# CORS 中间件
from fastapi.middleware.cors import CORSMiddleware
from .api.normal import router as normal_router
from .api.ai import router as ai_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有域名（开发用）
    allow_credentials=True,    # 允许携带 Cookie
    allow_methods=["*"],       # 允许所有请求方式
    allow_headers=["*"],       # 允许所有请求头
)


# 挂载两个接口（自动合并）
app.include_router(normal_router)
# app.include_router(ai_router)