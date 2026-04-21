from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 允许所有域名（开发用）
    allow_credentials=True,
    allow_methods=["*"],       # 允许所有请求方式
    allow_headers=["*"],       # 允许所有请求头
)

# 核心接口：去水印（内存流，不写文件）
@app.post("/remove-watermark")
async def remove_watermark(
    image: UploadFile,
    x: str = Form(...),
    y: str = Form(...),
    w: str = Form(...),
    h: str = Form(...)
):
    # 读取上传的图片内存字节
    image_bytes = await image.read()

    # FFmpeg 命令：从 stdin 读取 → 处理 → 输出到 stdout
    cmd = [
        "ffmpeg",
        "-i", "pipe:0",          # 从标准输入读（内存）
        "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}",
        "-update", "1",
        "-f", "image2pipe",      # 输出到标准输出（流）
        "-c", "png", # 输出 PNG 格式
        "pipe:1"                 # 输出流
    ]

    # 执行 FFmpeg，不生成任何文件
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 输入图片 → 获取输出流
    output_bytes, err = process.communicate(input=image_bytes)

    # 直接返回图片流给前端
    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png"
    )