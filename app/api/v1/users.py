from fastapi import APIRouter, Depends

from app.core.deps import get_user_role
from app.core.exceptions import get_or_404

from app.crud.user import UserCRUD

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session

users_router = APIRouter(prefix="/users", tags=["users"])
user_crud = UserCRUD()


@users_router.get("/role")
async def get_user_role(user_role: str = Depends(get_user_role)):
    return user_role


@users_router.get("/me")
async def get_user_role(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    user = get_or_404(user, detail="User not found")
    return user
