import uvicorn
from fastapi import FastAPI

from app.api.v1.main_routers import api_router

app = FastAPI(title="GreenChat", docs_url="/api/docs", openapi_url="/api")
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
