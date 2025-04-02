from collections.abc import Generator

from fastapi import HTTPException, Path
from src.core.enums.role import RoleEnum


def get_role_enum(role: str = Path(...)) -> Generator[RoleEnum, None, None]:
    role = role.lower()
    if role == "admin":
        yield RoleEnum.ADMIN
    elif role == "user":
        yield RoleEnum.USER
    else:
        raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
