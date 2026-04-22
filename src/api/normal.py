import base64
from fastapi import APIRouter
import subprocess
from src.schemas import InpaintRequest, Result

router = APIRouter()

# 现在入参 和 AI 接口完全一样！
@router.post("/remove-watermark", response_model=Result)
async def remove_watermark(req: InpaintRequest) -> Result:
    # 1. 解析前端传过来的 base64 图片
    image_base64 = req.image
    # 去掉 base64 前缀（data:image/png;base64,xxxx）
    if "base64," in image_base64:
        image_base64 = image_base64.split("base64,")[1]

    image_bytes = base64.b64decode(image_base64)

    # 2. 取 rects（和 AI 格式完全一样）
    rect = req.rects[0]
    x = rect.x
    y = rect.y
    w = rect.w
    h = rect.h

    # 3. FFmpeg 去水印（你原来的逻辑不动）
    cmd = [
        "ffmpeg",
        "-i", "pipe:0",
        "-vf", f"delogo=x={x}:y={y}:w={w}:h={h}",
        "-update", "1",
        "-f", "image2pipe",
        "-c", "png",
        "pipe:1"
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output_bytes, err = process.communicate(input=image_bytes)

    # 4. 输出转 base64
    output_base64 = base64.b64encode(output_bytes).decode("utf-8")

    # 5. 返回格式也和 AI 完全一样
    return Result(
        code=200,
        msg="普通去水印完成",
        data={
            "image": f"data:image/png;base64,{output_base64}"
        }
    )