from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Self, TypedDict
from typing import Any as typingAny

from .utils import MISSING

if TYPE_CHECKING:
    pass

__all__ = (
    "DBType",
    "Array",
    "Bool",
    "Datetime",
    "Float",
    "Int",
    "Number",
    "String",
    "Record",
)


class ManyResultResponseType(TypedDict):
    result: list[dict]
    time: str
    code: int | None
    description: str | None


class OneResultResponseType(TypedDict):
    result: dict
    time: str
    code: int | None
    description: str | None


class DBType:
    def __init__(
        self,
        *,
        sub_type: typingAny = MISSING,
        is_none: bool = False,
        _or: list[Self] = [],
    ):
        self.sub_type = sub_type
        self.__is_none = is_none
        self._or = None
        if self._or:
            self._or = " | ".join(str(__or) for __or in _or)

    def __repr__(self) -> str:
        value = self.__class__.__qualname__

        if self._or:
            value += f"{value} | {self._or}"

        if self.__is_none:
            return f"option<{value}>"

        else:
            return value

    def __str__(self) -> str:
        value = self.__class__.__qualname__

        if self.__is_none:
            return f"option<{value}>"
        else:
            return value


class Array(DBType):
    """リスト"""

    def __init__(self, sub_type: typingAny = MISSING):
        super().__init__(sub_type=sub_type)


class Bool(DBType):
    """真偽値"""

    def __init__(self):
        super().__init__()


class Datetime(DBType):
    """日時"""

    def __init__(self, datetime_format: str = "%Y/%m/%dT%H:%M:%SZ"):
        super().__init__()
        self.datetime_format = datetime_format

    def strftime(self, value: datetime):
        return value.strftime(self.datetime_format)


class Float(DBType):
    """小数"""

    def __init__(self):
        super().__init__()


class Int(DBType):
    """整数(64bit)"""

    def __init__(self):
        super().__init__()


class Number(DBType):
    """数値(自動変換)"""

    def __init__(self):
        super().__init__()


class String(DBType):
    """文字列"""

    def __init__(self):
        super().__init__()


class Object(DBType):
    """dict"""

    def __init__(self):
        super().__init__()


class Record(DBType):
    """レコード"""

    def __init__(self, sub_type: typingAny = MISSING):
        super().__init__(sub_type=sub_type)
