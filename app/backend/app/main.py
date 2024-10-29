import uvicorn
from fastapi import FastAPI

app = FastAPI(title="GreenChat", docs_url="/api/docs", openapi_url="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
