from fastapi import APIRouter, Depends

from app.crud.event import EventCRUD
from app.crud.event_member import EventMemberCRUD

from app.schemas.event import EventRead, EventCreate, EventUpdate, EventBase
from app.schemas.event_member import EventMemberRead

from app.db.models.event_member import MemberStatusEnum

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session

events_router = APIRouter(prefix="/events", tags=["events"])

event_crud = EventCRUD()
event_member_crud = EventMemberCRUD()


@events_router.get("/", response_model=list[EventRead])
async def get_events(db: AsyncSession = Depends(get_async_session)):
    events = await event_crud.get_all_events(db=db)
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
    member = await event_member_crud.set_member_status(
        db=db, event_id=event_id, user_id=user_id, status=MemberStatusEnum.ACCEPT
    )
    return member


@events_router.get("/{event_id}/members", response_model=list[EventMemberRead])
async def get_event_members(
    event_id: int, db: AsyncSession = Depends(get_async_session)
):
    members = await event_member_crud.get_event_members(db=db, event_id=event_id)
    return members
