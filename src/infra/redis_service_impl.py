import json
from typing import Any
from redis.asyncio import Redis

from src.core.exceptions.exceptions import ServiceError
from src.core.interface.redis_service import IRedisService


class RedisService(IRedisService):
    _host: str | None = None
    _port: int | None = None
    _db_number: int | None = None
    _connection: Redis | None = None

    @property
    def connection(self) -> Redis:
        if self._connection is None:
            raise NotImplementedError
        return self._connection

    def configure(self, host: str, port: int, db_number: int):
        self._host = host
        self._port = port
        self._db_number = db_number
        try:
            self._connection = Redis(host=self._host, port=self._port, db=self._db_number)
        except Exception as e:
            raise ServiceError("Fail make connection") from e

    async def ping(self) -> bool:
        return await self.connection.ping()

    async def set_str(self, *, key: str, value: str, ex: int | None = None) -> bool:
        if not isinstance(value, str):
            raise ServiceError("Method wait string value!")
        r = await self.connection.set(key, value=value, ex=ex)
        if not r:
            raise ServiceError(f"Value: {value} is not set!")
        return r

    async def get_str(self, *, key: str) -> str | None:
        r = await self.connection.get(key)
        if r is None:
            return None
        value = r.decode()
        if not isinstance(value, str):
            raise ServiceError("Method wait string value!")
        return value

    async def set_dict(
        self, *, key: str, value: dict[Any, Any], ex: int | None = None
    ) -> bool:
        if not isinstance(value, list | dict | str):
            raise ServiceError("Method wait list, str, dict value")
        data_str = json.dumps(value)
        return await self.set_str(key=key, value=data_str, ex=ex)

    async def get_dict(self, *, key: str) -> dict[Any, Any] | None | str | list[Any]:
        r = await self.connection.get(key)
        if r is None:
            return None
        data = json.loads(r)
        if not isinstance(data, list | str | dict):
            raise ServiceError("Method wait list, str, dict value!")
        return data

    async def delete(self, *, key: str) -> bool:
        r = await self.connection.delete(key)
        return bool(r)


service_redis = RedisService()
