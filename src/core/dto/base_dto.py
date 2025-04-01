from dataclasses import dataclass, asdict
from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from typing import get_type_hints, get_args, get_origin


@dataclass
class BaseDTO:
    """Базовый DTO с методами для работы с dict."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Создает DTO из словаря."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Конвертирует DTO в словарь."""
        return asdict(self)


T = TypeVar("T", bound=BaseDTO)


@dataclass
class BaseListDTO(Generic[T]):
    """Базовый DTO для списков с пагинацией"""

    items: Sequence[T]
    total: int | None = None
    offset: int = 0
    limit: int = 100

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Создает DTO из словаря, рекурсивно преобразуя элементы items в DTO."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")

        data = data.copy()
        items = data.pop("items", [])

        # Определяем тип элементов (T) из Generic
        item_type = cls._get_item_type()

        # Преобразуем каждый элемент в DTO, если он еще не DTO
        converted_items = [
            item if isinstance(item, item_type) else item_type.from_dict(item)
            for item in items
        ]

        return cls(items=converted_items, **data)

    def to_dict(self) -> dict[str, Any]:
        """Конвертирует DTO в словарь, рекурсивно преобразуя вложенные DTO."""
        result = asdict(self)

        # Рекурсивно преобразуем элементы items в dict, если они DTO
        result["items"] = [
            item.to_dict() if isinstance(item, BaseDTO) else item for item in self.items
        ]

        return result

    @classmethod
    def _get_item_type(cls) -> type:
        """Получает тип элементов (T) из Generic."""
        type_hints = get_type_hints(cls)
        item_type = type_hints.get("items", Any)

        # Если items: Sequence[T], извлекаем T
        if get_origin(item_type) is Sequence:
            item_type = get_args(item_type)[0]

        return item_type
