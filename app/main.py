from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine, get_async_session

from app.api import api_router

import app.db.models  # type: ignore


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
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

app.include_router(api_router)


@app.get("/status")
async def root():
    return {"status": "ok"}


@app.post("/db-status")
async def db_access(db: AsyncSession = Depends(get_async_session)):
    return {"status": "ok"}
