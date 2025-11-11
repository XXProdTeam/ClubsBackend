from app.db.models.user import User

from app.schemas.user import UserCreate

from app.db.models.user import UserRoleEnum

from app.core.exceptions import get_or_404

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserCRUD:
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        query = select(User).where(User.user_id == user_id)
        result = await db.execute(query)
        return get_or_404(result.scalar_one_or_none(), detail="User not found")

    async def create_user(self, db: AsyncSession, user: UserCreate) -> User:
        new_user = User(
            **user.model_dump(exclude_unset=True),
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        user = await self.get_user_by_id(db, user_id)
        await db.delete(user)
        await db.commit()

    async def set_user_role(
        self, db: AsyncSession, user_id: int, role: UserRoleEnum
    ) -> User:
        user = await self.get_user_by_id(db, user_id)
        user.role = role
        await db.commit()
        await db.refresh(user)
        return user
