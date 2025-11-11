from fastapi import HTTPException

from app.db.models.event_member import EventMember

from app.schemas.event_member import EventMemberCreate

from app.crud.event import EventCRUD
from app.crud.user import UserCRUD

from app.db.models.event_member import MemberStatusEnum

from app.core.exceptions import get_or_404

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

event_crud = EventCRUD()
user_crud = UserCRUD()


class EventMemberCRUD:
    def __init__(self):
        self.event_crud = EventCRUD()

    async def create_event_member(
        self, db: AsyncSession, event_member: EventMemberCreate
    ) -> EventMember:
        members = await self.get_event_members(db=db, event_id=event_member.event_id)

        event = await self.event_crud.get_event_by_id(
            db=db, event_id=event_member.event_id
        )
        user = await user_crud.get_user_by_id(db=db, user_id=event_member.user_id)

        if user.role not in event.audience:
            raise HTTPException(
                status_code=403, detail="User is not allowed to do this"
            )

        if event_member.user_id in [member.user_id for member in members]:
            raise HTTPException(status_code=400, detail="User already in member list")

        if len(members) >= event.member_limit:
            raise HTTPException(status_code=400, detail="Event is full")

        new_event_member = EventMember(**event_member.model_dump(exclude_unset=True))
        db.add(new_event_member)
        await db.commit()
        await db.refresh(new_event_member)
        return new_event_member

    async def get_event_members(self, db: AsyncSession, event_id: int):
        query = select(EventMember).where(EventMember.event_id == event_id)
        result = await db.execute(query)
        return get_or_404(result.scalars().all(), detail="Members or Event not found")

    async def get_event_member(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> EventMember:
        query = select(EventMember).where(
            EventMember.user_id == user_id, EventMember.event_id == event_id
        )
        result = await db.execute(query)
        return get_or_404(
            result.scalar_one_or_none(), detail="User or Event not found in member list"
        )

    async def get_members_events(
        self, db: AsyncSession, user_id: int
    ) -> list[EventMember]:
        query = select(EventMember).where(EventMember.user_id == user_id)
        result = await db.execute(query)
        return get_or_404(result.scalars().all(), detail="Events not found")

    async def delete_event_member(
        self, db: AsyncSession, user_id: int, event_id: int
    ) -> None:
        member = await self.get_event_member(db=db, user_id=user_id, event_id=event_id)
        await db.delete(member)
        await db.commit()

    async def set_member_status(
        self, db: AsyncSession, user_id: int, event_id: int, status: MemberStatusEnum
    ) -> EventMember:
        member = await self.get_event_member(db=db, user_id=user_id, event_id=event_id)

        member.status = status
        await db.commit()
        await db.refresh(member)
        return member
