from fastapi import APIRouter


router = APIRouter()


@router.get(
    "/con",
    responses={200: {"model": dict}},
)
async def healthcheck():
    return {"yes": "that worked"}
