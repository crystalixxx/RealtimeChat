import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.main_routers import api_router

app = FastAPI(title="GreenChat", docs_url="/api/docs", openapi_url="/api")
app.include_router(api_router)

# origins = [
#     "http://localhost:8000",
#     "http://localhost:80",
#     "http://frontend:5173",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
