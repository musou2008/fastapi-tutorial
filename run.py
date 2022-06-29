import uvicorn
from fastapi import FastAPI
from tutorial import app03, app04, app05, app06, app07, app08

app = FastAPI()

app.include_router(app03, prefix="/chapter03",tags=["第3章 请求参数和验证"])
app.include_router(app03, prefix="/chapter04",tags=["第4章 响应处理和FastAPI配置"])
app.include_router(app03, prefix="/chapter05",tags=["第5章 FastAPI的依赖注入系统"])
app.include_router(app03, prefix="/chapter06",tags=["第6章 安全、认证和授权"])
app.include_router(app03, prefix="/chapter07",tags=["第7章 FastAPI的数据库操作和多应用的目录结构设计"])
app.include_router(app03, prefix="/chapter08",tags=["第8章 中间件、CORS、后台任务、测试用例"])

if __name__ == "__main__":
    uvicorn.run(
        "run:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=1
    )
