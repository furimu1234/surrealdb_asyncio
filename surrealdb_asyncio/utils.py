from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import ValidationInfo

    from ._types import DBType
    from .query import Query

__all__ = (
    "MISSING",
    "validate",
    "log",
    "log_sql",
    "log_res",
    "log_select",
    "log_insert",
    "log_update",
    "log_delete",
)

log = logging.getLogger(__name__)


def log_sql(q: Query, _type: str):
    """実行するsqlのログ"""
    log.debug(f"======DEBUG {_type}======")
    log.debug(q.to_string())
    log.debug("=============")


def log_select(q: Query):
    """ログ"""
    log_sql(q, "SELECT")


def log_insert(q: Query):
    """ログ"""
    log_sql(q, "INSERT")


def log_update(q: Query):
    """ログ"""
    log_sql(q, "UPDATE")


def log_delete(q: Query):
    """ログ"""
    log_sql(q, "DELETE")


def log_res(res):
    """レスポンスログ"""
    log.debug(res)
    log.debug("=============")


def validate(v: DBType, info: ValidationInfo):
    """pydantic BaseModelでstrやdictに変換できない型を定義する用"""
    return v


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()
