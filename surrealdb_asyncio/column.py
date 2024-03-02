from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Generic, Self, TypeVar

from pydantic import BaseModel, PlainValidator

from ._types import Array, Bool, Datetime, DBType, Float, Int, Number, String
from .table import BaseTable
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

    def add_quotation(self, v: String | str | None = None):
        return f"'{v or self.value}'"

    def list_join(self, value: list | None = None):
        sql = ""

        for v in value or self.value:
            if isinstance(v, str):
                sql += f"{self.add_quotation(v)}"

            elif isinstance(v, list):
                if not v:
                    continue

                elif isinstance(v[0], datetime) and isinstance(v[1], str):
                    datetime_value = v[0].strftime(v[1])
                    sql += f"'{datetime_value}'"
                    continue

                elif isinstance(v[0], list):
                    sql += self.list_join(v[0])
                    continue

                sql += self.list_join(v)

            elif isinstance(v, BaseTable):
                sql += f"{v.table_name}"

        return sql

    def to_sql_value(self):
        """sqlでそのまま使える文字列を返す"""

        if isinstance(self.type, String):
            return f"{self.add_quotation()}"

        elif isinstance(
            self.type,
            (
                Int,
                Number,
                Bool,
                Float,
            ),
        ):
            return f"{self.value}"
        elif isinstance(self.type, Array):
            return f"{self.list_join()}"

        elif isinstance(self.type, Datetime):
            value = self.value.strftime(self.type.datetime_format)
            return f"'{value}'"
        return self.value
