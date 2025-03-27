from fastapi import APIRouter

from . import hc

router = APIRouter(
    prefix="/helthcheck",
    tags=["Healthcheck v1"],
)
router.include_router(hc.router)
