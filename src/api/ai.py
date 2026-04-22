import io
import base64
from fastapi import HTTPException, APIRouter
# 图像处理
from PIL import Image, ImageDraw
# 模型
from simple_lama_inpainting import SimpleLama

from src.schemas import InpaintRequest, Result

router = APIRouter();
model = SimpleLama()


@router.post("/remove-watermark-ai", response_model=Result)
async def remove_watermark(data: InpaintRequest) -> Result:
    try:
        # ==========================
        # 调试输出（关键！）
        # ==========================
        print("📥 收到请求")
        print("image 长度:", len(data.image))
        print("rects:", data.rects)

        # 解析 Base64
        if "," in data.image:
            header, encoded = data.image.split(",", 1)
        else:
            encoded = data.image
        
        print("✅ Base64 分割成功")

        img_bytes = base64.b64decode(encoded)
     
        print("✅ img_bytes 分割成功")
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        print("✅ convert 分割成功")


        print("✅ 图片解析成功:", img.size)

        # 绘制掩码
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        padding = 3

        for rect in data.rects:
            x0 = int(rect.x - padding)
            y0 = int(rect.y - padding)
            x1 = int(rect.x + rect.w + padding)
            y1 = int(rect.y + rect.h + padding)
            draw.rectangle([x0, y0, x1, y1], fill=255)

            print(f"✅ 绘制框：x={x0}, y={y0}, w={x1-x0}, h={y1-y0}")

        # 模型运行
        print("🔍 开始 LaMa 去水印")
        result_img = model(img, mask)
        print("✅ 处理完成！")

        # 返回 Base64
        buffered = io.BytesIO()
        result_img.save(buffered, format="PNG")
        output_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return Result(
            code=200,
            msg="处理成功",
            data={"image": f"data:image/png;base64,{output_base64}"}
        )

    except Exception as e:
        print("❌ 错误信息:", str(e))
        raise HTTPException(status_code=500, detail=str(e))