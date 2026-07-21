from fastapi import FastAPI

from app.api.routes import health, inventory, warehouses
from app.core.config import settings
SERVICE_PREFIX = f"/{settings.service_name}"


app = FastAPI(title=settings.service_name)

app.include_router(health.router, prefix=f"{SERVICE_PREFIX}/health", tags=["health"])
app.include_router(warehouses.router, prefix=f"{SERVICE_PREFIX}/warehouses", tags=["warehouses"])
app.include_router(inventory.router, prefix=f"{SERVICE_PREFIX}/inventory", tags=["inventory"])


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.service_name, "status": "running"}
