from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.event import EventCRUD
from app.crud.event_member import EventMemberCRUD
from app.crud.user import UserCRUD

from app.schemas.event import EventRead, EventCreate, EventUpdate, EventBase
from app.schemas.event_member import EventMemberRead

from app.db.models.event_member import MemberStatusEnum

from app.db.session import get_async_session

from app.services.scheduler_service import ScheduleService


events_router = APIRouter(prefix="/events", tags=["events"])

user_crud = UserCRUD()
event_crud = EventCRUD()
event_member_crud = EventMemberCRUD()

schedule_service = ScheduleService()


@events_router.get("/", response_model=list[EventRead])
async def get_events(
    is_actual: bool = True, db: AsyncSession = Depends(get_async_session)
):
    events = await event_crud.get_all_events(db=db, actual=is_actual)
    for event in events:
        members = await event_member_crud.get_event_members(
            db=db, event_id=event.event_id
        )
        event.num_members = len(members)
    return events


@events_router.get("/{event_id}", response_model=EventRead)
async def get_event_by_id(event_id: int, db: AsyncSession = Depends(get_async_session)):
    event = await event_crud.get_event_by_id(db=db, event_id=event_id)
    members = await event_member_crud.get_event_members(db=db, event_id=event_id)
    event.num_members = len(members)
    return event


@events_router.post("/", response_model=EventCreate)
async def create_event(
    new_event: EventCreate, db: AsyncSession = Depends(get_async_session)
):
    new_event = await event_crud.create_event(db=db, event=new_event)
    return new_event


@events_router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_async_session)):
    await event_crud.delete_event(db=db, event_id=event_id)


@events_router.patch("/{event_id}", response_model=EventBase)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    updated_event = await event_crud.update_event(
        db=db, event_id=event_id, event_update=event_update
    )
    return updated_event


@events_router.post("/{event_id}/register/{user_id}", response_model=EventMemberRead)
async def register_user_for_event(
    event_id: int, user_id: int, db: AsyncSession = Depends(get_async_session)
):
    existing_member = await event_member_crud.get_event_member(
        db=db, event_id=event_id, user_id=user_id
    )
    if existing_member.status == MemberStatusEnum.ACCEPT:
        raise HTTPException(status_code=400, detail="User is already registered")

    member = await event_member_crud.set_member_status(
        db=db, event_id=event_id, user_id=user_id, status=MemberStatusEnum.ACCEPT
    )
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    event = await event_crud.get_event_by_id(db=db, event_id=event_id)
    if event.feedback_link:
        schedule_service.schedule_reminder_feedback_link(
            event_id=event_id, user_id=user_id, remind_time=event.end_time
        )
    member.first_name = user.first_name
    member.last_name = user.last_name
    return member


@events_router.get("/{event_id}/members", response_model=list[EventMemberRead])
async def get_event_members(
    event_id: int, db: AsyncSession = Depends(get_async_session)
):
    response_members = []
    members = await event_member_crud.get_event_members(db=db, event_id=event_id)
    for member in members:
        user = await user_crud.get_user_by_id(db=db, user_id=member.user_id)
        member.first_name = user.first_name
        member.last_name = user.last_name
        response_members.append(member)
    return response_members
