from fastapi import APIRouter, Depends, HTTPException

from src.core.usecases import get_user_usecase
from src.core.usecases import get_many_user_usecase
from src.core.interface.password_hasher import IPasswordHasher
from src.application.depends.provider import get_password_hasher, get_uow_sql
from src.core.interface.uow.uow_sql import IUowSQL
from src.core.usecases import create_user_usecase
from src.core.dto.user import UserCreateDTO
from src.core.exceptions.exceptions import MappingError
from src.core.schemas.user import ListUserSchema, UserCreateSchema, UserSchema

router = APIRouter()


@router.post(
    "/users",
    responses={
        201: {"model": UserSchema},
    },
)
async def create_user(
    data: UserCreateSchema,
    uow_sql: IUowSQL = Depends(get_uow_sql),
    hasher: IPasswordHasher = Depends(get_password_hasher),
):
    try:
        data_res = data.dict()
        dto = UserCreateDTO(**data_res)
    except Exception as e:
        raise MappingError(f"Mapping error. Schema: error: {e}") from e
    try:
        uc = create_user_usecase.Usecase(uow_sql=uow_sql, password_hasher=hasher)
        res = await uc(dto=dto)
        response_schema = UserSchema(**res.to_dict())

        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail="Conflict",
        ) from e


@router.get(
    "/users",
    responses={
        200: {"model": ListUserSchema},
    },
)
async def get_many_users(uow_sql: IUowSQL = Depends(get_uow_sql)):
    try:
        uc = get_many_user_usecase.Usecase(uow_sql=uow_sql)
        res = await uc()
        response_schema = ListUserSchema(**res.to_dict())
        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Error",
        ) from e


@router.get(
    "/users/{user_id}",
    responses={
        200: {"model": UserSchema},
    },
)
async def get_user(user_id: int, uow_sql: IUowSQL = Depends(get_uow_sql)):
    try:
        uc = get_user_usecase.Usecase(uow_sql=uow_sql)
        res = await uc(user_id=user_id)
        response_schema = UserSchema(**res.to_dict())
        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Not Found",
        ) from e
