from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_session_local

router = APIRouter()


@router.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/db")
def database_health_check() -> dict[str, str]:
    try:
        session_local = get_session_local()
        with session_local() as db:
            db.execute(text("SELECT 1"))
    except (RuntimeError, SQLAlchemyError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {"database": "ok"}
