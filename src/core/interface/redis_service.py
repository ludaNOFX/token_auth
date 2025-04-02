from abc import ABC, abstractmethod
from typing import Any
from redis.asyncio import Redis


class IRedisService(ABC):
    _host: str | None = None
    _port: int | None = None
    _db_number: int | None = None
    _connection: Redis | None = None

    @property
    @abstractmethod
    def connection(self) -> Redis: ...

    @abstractmethod
    def configure(self, host: str, port: int, db_number: int): ...

    @abstractmethod
    async def ping(self) -> bool: ...

    @abstractmethod
    async def set_str(self, *, key: str, value: str, ex: int | None = None) -> bool: ...

    @abstractmethod
    async def get_str(self, *, key: str) -> str | None: ...

    @abstractmethod
    async def set_dict(
        self, *, key: str, value: dict[Any, Any], ex: int | None = None
    ) -> bool: ...

    @abstractmethod
    async def get_dict(self, *, key: str) -> dict[Any, Any] | None | str | list[Any]: ...

    @abstractmethod
    async def delete(self, *, key: str) -> bool: ...
