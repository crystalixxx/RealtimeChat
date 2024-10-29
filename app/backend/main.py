import uvicorn
from fastapi import FastAPI

app = FastAPI(title="GreenChat", docs_url="/api/docs", openapi_url="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, reload=True)
