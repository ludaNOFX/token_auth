from fastapi import APIRouter, Depends, HTTPException

from src.core.enums.role import RoleEnum
from src.core.usecases import get_role_usecase
from src.application.api.dependencies.role import get_role_enum
from src.core.usecases import get_many_roles_usecase
from src.core.schemas.role import ListRoleSchema, RoleCreateSchema, RoleSchema
from src.core.usecases import create_role_usecase
from src.core.dto.role import RoleCreateDTO
from src.application.depends.provider import get_uow_sql
from src.core.interface.uow.uow_sql import IUowSQL
from src.core.exceptions.exceptions import MappingError

router = APIRouter()


@router.post(
    "/roles",
    responses={
        201: {"model": RoleSchema},
    },
)
async def create_role(data: RoleCreateSchema, uow_sql: IUowSQL = Depends(get_uow_sql)):
    try:
        data_res = data.dict()
        dto = RoleCreateDTO(**data_res)

    except Exception as e:
        raise MappingError(f"Mapping error. Schema: error: {e}") from e
    try:
        uc = create_role_usecase.Usecase(uow_sql=uow_sql)
        res = await uc(dto=dto)
        response_schema = RoleSchema(**res.to_dict())

        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail="Conflict",
        ) from e


@router.get(
    "/roles",
    responses={
        200: {"model": ListRoleSchema},
    },
)
async def get_many_roles(uow_sql: IUowSQL = Depends(get_uow_sql)):
    try:
        uc = get_many_roles_usecase.Usecase(uow_sql=uow_sql)
        res = await uc()
        response_schema = ListRoleSchema(**res.to_dict())
        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Error",
        ) from e


@router.get(
    "/roles/{role}",
    responses={
        200: {"model": RoleSchema},
    },
)
async def get_role(
    role: RoleEnum = Depends(get_role_enum), uow_sql: IUowSQL = Depends(get_uow_sql)
):
    try:
        uc = get_role_usecase.Usecase(uow_sql=uow_sql)
        res = await uc(role=role)
        response_schema = RoleSchema(**res.to_dict())
        return response_schema
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Not Found",
        ) from e
