from fastapi import APIRouter

from . import roles

router = APIRouter(
    prefix="/roles",
    tags=["Roles v1"],
)

router.include_router(roles.router)
