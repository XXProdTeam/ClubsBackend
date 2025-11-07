from fastapi import APIRouter

from app.api.v1.users import users_router
from app.api.v1.events import events_router

subrouters = (
    users_router,
    events_router,
)

v1_router = APIRouter(prefix="/v1")

for subrouter in subrouters:
    v1_router.include_router(subrouter)
