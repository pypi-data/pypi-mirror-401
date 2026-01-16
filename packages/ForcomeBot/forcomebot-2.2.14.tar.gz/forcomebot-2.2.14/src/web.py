"""
旧版Web管理界面（已废弃）
保留此模块以兼容旧版代码，实际功能已迁移到 React 前端
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["admin"])

# 全局引用（兼容旧版代码）
_handler = None
_scheduler = None
_config = None


def set_references(handler, scheduler, config):
    """设置全局引用（兼容旧版代码）"""
    global _handler, _scheduler, _config
    _handler = handler
    _scheduler = scheduler
    _config = config


@router.get("/", response_class=HTMLResponse)
async def admin_page():
    """旧版管理界面入口 - 重定向到新版 React 前端"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>FORCOME 康康 - 管理界面</title>
        <meta http-equiv="refresh" content="0;url=/app/">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: #f5f5f5;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            a {
                color: #2563eb;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>正在跳转到新版管理界面...</h2>
            <p>如果没有自动跳转，请点击 <a href="/app/">这里</a></p>
        </div>
    </body>
    </html>
    """
