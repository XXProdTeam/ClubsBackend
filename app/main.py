from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.session import engine, get_async_session

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


@app.get("/status")
async def root():
    return {"status": "ok"}


@app.get("/qrcode")
async def generate_base64_qrcode():
    from app.services.image_client import generate_qr_code, image_to_base64

    qr_image = generate_qr_code(data={"url": "https://google.com", "qr_size": 100})
    base64_image = image_to_base64(qr_image)

    return base64_image


@app.post("/db-status")
async def db_access(db: AsyncSession = Depends(get_async_session)):
    return {"status": "ok"}
