from pathlib import Path
import sys

import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",  # 模块路径: app 对象
        host="0.0.0.0",           # 局域网可访问
        port=8000,                # 端口
        reload=True,              # 开发热重载
        log_level="info"
    )