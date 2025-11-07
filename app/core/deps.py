from app.crud.user import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.db.session import get_async_session

user_crud = UserCRUD()


async def get_user_role(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    return user.role
