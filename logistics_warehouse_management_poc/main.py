from fastapi import FastAPI
from app.routers.products import router

app = FastAPI(
    title="Logistics POC API",
    version ="1.0.0",
    description="A Poc for managing products."
)

app.include_router(router,prefix="/api/product")