from fastapi import APIRouter, Depends

from app.crud.user import UserCRUD
from app.db.models.user import UserRoleEnum
from app.schemas.user import UserRead, UserCreate

from app.services import image_client

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session

users_router = APIRouter(prefix="/users", tags=["users"])
user_crud = UserCRUD()


@users_router.get("/me", response_model=UserRead)
async def get_user_role(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    return user


@users_router.get("/me/qr")
async def generate_base64_qrcode(
    user_id: int, db: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    user_data = UserRead.model_validate(user).model_dump()
    qr_image = image_client.generate_qr_code(data=user_data)
    base64_image = image_client.image_to_base64(qr_image)

    return {"base64_str": base64_image}


@users_router.post("/register", status_code=201, response_model=UserCreate)
async def register_user(
    new_user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    await user_crud.create_user(db=db, user=new_user)
    return new_user


@users_router.post("/role/{role}")
async def set_user_role(
    role: UserRoleEnum, user_id: int, db: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    user.role = role
    await db.commit()
    return {"user_id": user.user_id, "new_role": user.role}

@users_router.get("/events")
async def get_user_events(user_id: int, db: AsyncSession = Depends(get_async_session)):
    pass