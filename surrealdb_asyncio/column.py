from __future__ import annotations

from typing import Annotated, Any, Generic, Self, TypeVar

from pydantic import BaseModel, PlainValidator

from ._types import DBType
from .utils import validate

__all__ = ("Column",)

T = TypeVar("T")


class Column(BaseModel, Generic[T]):
    name: str | None = None
    type: Annotated[DBType, PlainValidator(validate)]  # OR未対応
    print()
    value: Any = None
    datetime_format: str = "%Y/%m/%dT%H:%M:%SZ"

    def __str__(self):
        return str(self.value)

    def set_value(self, new_value: T) -> Self:
        self.value = new_value
        return self

    def get_value(self) -> T:
        return self.value
