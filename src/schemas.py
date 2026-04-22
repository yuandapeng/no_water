from typing import List

from pydantic import BaseModel

# 统一接口返回格式（企业万能响应）
class Result(BaseModel):
    code: int       # 状态码
    msg: str        # 提示信息
    data: dict | None = None  # 返回数据

class Rect(BaseModel):
    x: float
    y: float
    w: float
    h: float

class InpaintRequest(BaseModel):
    image: str
    rects: List[Rect]
