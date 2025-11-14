from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import UserCRUD
from app.crud.event import EventCRUD
from app.crud.event_member import EventMemberCRUD

from app.db.models.user import UserRoleEnum

from app.db.session import get_async_session

from app.schemas.event_member import EventMemberCreate, EventMemberRead
from app.schemas.user import UserRead, UserCreate
from app.schemas.event import EventRead, EventMemberResponse

from app.services.image_service import generate_qr_code, image_to_base64
from app.services.bot_notification_service import NotificationService
from app.services.bot_file_service import FileService
from app.services.scheduler_service import ScheduleService


users_router = APIRouter(prefix="/users", tags=["users"])

user_crud = UserCRUD()
event_crud = EventCRUD()
event_member_crud = EventMemberCRUD()

bot_notification_service = NotificationService()
bot_file_service = FileService()
schedule_service = ScheduleService()


@users_router.post("/register", status_code=201, response_model=UserCreate)
async def register_user(
    new_user: UserCreate, db: AsyncSession = Depends(get_async_session)
):
    await user_crud.create_user(db=db, user=new_user)
    return new_user


@users_router.get("/me", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    return user


@users_router.get("/me/events", response_model=list[EventRead])
async def get_user_registered_events(
    user_id: int, is_actual: bool = True, db: AsyncSession = Depends(get_async_session)
):
    event_members = await event_member_crud.get_members_events(db=db, user_id=user_id)
    events_response = []
    for event_member in event_members:
        event = await event_crud.get_event_by_id(db=db, event_id=event_member.event_id)
        members = await event_member_crud.get_event_members(
            db=db, event_id=event.event_id
        )
        event.num_members = len(members)
        events_response.append(event)
    if is_actual:
        events_response.sort(key=lambda x: x.start_time)
    return events_response


@users_router.get("/me/qr", response_model=dict[str, str])
async def generate_base64_qrcode(
    user_id: int, db: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    user_data = UserRead.model_validate(user).model_dump()
    qr_image = generate_qr_code(data=user_data)
    base64_image = image_to_base64(qr_image)

    return {"base64_str": base64_image}


@users_router.post("/role/{role}", response_model=UserRead)
async def set_user_role(
    role: UserRoleEnum, user_id: int, db: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.set_user_role(db=db, user_id=user_id, role=role)
    return user


@users_router.get("/events", response_model=list[EventRead])
async def get_all_events_for_user(
    user_id: int, is_actual: bool = True, db: AsyncSession = Depends(get_async_session)
):
    events = await event_crud.get_all_events_for_user(
        db=db, user_id=user_id, actual=is_actual
    )
    for event in events:
        members = await event_member_crud.get_event_members(
            db=db, event_id=event.event_id
        )
        event.num_members = len(members)
    return events


@users_router.get("/events/{event_id}", response_model=EventMemberResponse)
async def get_users_event_by_id(
    user_id: int, event_id: int, db: AsyncSession = Depends(get_async_session)
):
    event = await event_crud.get_event_by_id(db=db, event_id=event_id)
    members = await event_member_crud.get_event_members(db=db, event_id=event_id)
    event.num_members = len(members)

    is_member = await event_member_crud.is_user_member(
        db=db, user_id=user_id, event_id=event_id
    )
    event.is_member = is_member
    return event


@users_router.get("/events/{event_id}/ics")
async def get_ics_for_event(
    user_id: int, event_id: int, db: AsyncSession = Depends(get_async_session)
):
    await bot_file_service.send_ics(db=db, user_id=user_id, event_id=event_id)


@users_router.post(
    "/events/{event_id}/register", status_code=201, response_model=EventMemberRead
)
async def register_user_for_event(
    user_id: int, event_id: int, db: AsyncSession = Depends(get_async_session)
):
    new_event_member = EventMemberCreate(user_id=user_id, event_id=event_id)
    user = await user_crud.get_user_by_id(db=db, user_id=user_id)
    event = await event_crud.get_event_by_id(db=db, event_id=event_id)
    new_member = await event_member_crud.create_event_member(
        db=db, event_member=new_event_member
    )
    new_member.first_name = user.first_name
    new_member.last_name = user.last_name

    await bot_notification_service.register_event(
        db=db, user_id=user_id, event_id=event_id
    )
    schedule_service.schedule_reminder_one_day_before(
        event_id=event_id, user_id=user_id, remind_time=event.start_time
    )

    schedule_service.schedule_reminder_one_hour_before(
        event_id=event_id,
        user_id=user_id,
        remind_time=event.start_time,
    )
    return new_member


@users_router.delete("/events/{event_id}/register", status_code=204)
async def unregister_user_from_event(
    user_id: int, event_id: int, db: AsyncSession = Depends(get_async_session)
):
    await event_member_crud.delete_event_member(
        db=db, user_id=user_id, event_id=event_id
    )
    await bot_notification_service.unregister_event(
        db=db, user_id=user_id, event_id=event_id
    )
