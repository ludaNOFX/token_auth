from fastapi import APIRouter

from . import users

router = APIRouter(
    prefix="/users",
    tags=["Users v1"],
)

router.include_router(users.router)
