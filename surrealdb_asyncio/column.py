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
    value: Any = None
    datetime_format: str = "%Y/%m/%dT%H:%M:%SZ"

    def __str__(self):
        return str(self.value)

    def set_value(self, new_value: T) -> Self:
        """valueに値を設定する。型ヒントが欲しい時用

        Parameters
        ----------
        new_value : T
            設定する値

        Returns
        -------
        Self
            インスタンス
        """
        self.value = new_value
        return self

    def get_value(self) -> T:
        """値を取得する。型ヒントが欲しい時用

        Returns
        -------
        T
            値
        """

        return self.value
