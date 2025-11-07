from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.db.base import Base
from app.db.session import engine, get_async_session

import app.db.models  # type: ignore


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings()  # type: ignore
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/config")
async def show_config():
    settings = Settings()  # type: ignore
    return {
        "database_url": settings.DATABASE_URL,
        "host": settings.POSTGRES_HOST,
        "user": settings.POSTGRES_USER,
        "db": settings.POSTGRES_DB,
    }


@app.post("/")
async def db_access(db: AsyncSession = Depends(get_async_session)):
    return {"status": "ok"}
