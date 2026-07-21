from fastapi import FastAPI

from app.api.routes import health, users
from app.core.config import settings


app = FastAPI(title=settings.service_name)

app.include_router(health.router)
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def root() -> dict[str, str]:
    return {"service": settings.service_name, "status": "running"}
