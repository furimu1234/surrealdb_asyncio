from __future__ import annotations

import os
from typing import Self

import aiohttp
from pydantic import BaseModel, Field, model_validator

from ._types import ManyResultResponseType, OneResultResponseType
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


__all__ = ("BaseTable",)

DB = os.environ.get("SurrealDB_HOST")
USER = os.environ.get("SurrealDB_USER")
PASSWORD = os.environ.get("SurrealDB_PASSWORD")


assert isinstance(DB, str)
assert isinstance(USER, str)
assert isinstance(PASSWORD, str)


class BaseTable(BaseModel):
    table_name: str = Field(default="", exclude=True)
    id: str | int | None = Field(default=None, exclude=True)
    ns: str = Field(default="test", exclude=True)
    db: str = Field(default="test", exclude=True)
    db: str = Field(default=DB, exclude=True)
    user: str = Field(default=USER, exclude=True)
    password: str = Field(default=PASSWORD, exclude=True)

    @model_validator(mode="after")
    def create_table_name(self) -> Self:
        self.table_name = self.__class__.__qualname__.lower()

        if self.id is not None:
            self.table_name += ":" + str(self.id)

        return self

    async def executes(self, sql: str) -> ManyResultResponseType:
        headers = {"Accept": "application/json", "ns": self.ns, "db": self.db}

        async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(login=self.user, password=self.password)
        ) as session:
            async with session.post(
                self.db + "/sql",
                data=sql,
                headers=headers,
            ) as response:
                response_data = await response.json()

                if isinstance(response_data, dict):
                    raise Exception(response_data)
                else:
                    return response_data[0]

    async def execute(self, sql: str) -> OneResultResponseType:
        response = await self.executes(sql)
        return {
            "code": response.get("code", ""),
            "result": response.get("result", ""),  # type: ignore
            "description": response.get("description", ""),
            "time": response["time"],
        }
