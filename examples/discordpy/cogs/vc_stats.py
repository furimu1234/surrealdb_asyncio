from typing import Self

import discord
from discord.ext import commands

from surrealdb_asyncio import BaseTable, Column, Query
from surrealdb_asyncio._types import Float, Int


class VC_Stats(BaseTable):
    connect_time: Column[float] = Column(name="connect_time", type=Float(), value=0)
    server_id: Column[int] = Column(name="server_id", type=Int())

    def set_data(self, res: dict) -> Self:
        self.server_id.set_value(res.get("server_id", 0))
        self.connect_time.set_value(res.get("connect_time", 0))
        return self

    async def fetch(self) -> Self:
        q = Query()
        q.select(self)
        q.where(f"server_id = {self.server_id}")

        res = (await self.executes(q.to_string()))["result"]

        if not res:
            return self
        else:
            self.is_none = False
            return self.set_data(res[0])

    async def insert(self) -> Self:
        q = Query()
        q.insert(self)
        q.add_sqlvalue(self.server_id)
        q.add_sqlvalue(self.connect_time)

        res = (await self.executes(q.to_string()))["result"]
        if not res:
            return self
        else:
            self.is_none = False
            return self.set_data(res[0])

    async def update(self) -> Self:
        q = Query()
        q.update(self)
        q.add_sqlvalue(self.server_id)
        q.add_sqlvalue(self.connect_time)

        res = (await self.executes(q.to_string()))["result"]
        if not res:
            return self
        else:
            self.is_none = False
            return self.set_data(res[0])

    async def delete(self) -> Self:
        q = Query()
        q.delete(self)
        q.where(f"server_id = {self.server_id}")

        res = (await self.executes(q.to_string()))["result"]
        if not res:
            return self
        else:
            self.is_none = False
            return self.set_data(res[0])


class VcStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connect_time_cache = {}

    def convert_str_usertime(self, td: float):
        days = td // (24 * 3600)
        remaining_seconds = td % (24 * 3600)

        hours = remaining_seconds // 3600
        remaining_seconds %= 3600

        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        return f"{days:.0f}日 {hours:.0f}時間{minutes:.0f}分{seconds:.0f}秒"

    @commands.hybrid_command(name="接続時間確認")
    async def show(self, ctx: commands.Context):
        """コマンド送信者の接続時間を表示する"""
        if not ctx.guild:
            return

        db = VC_Stats(id=ctx.author.id)
        db.server_id.set_value(ctx.guild.id)

        await db.fetch()

        desc = f"### {ctx.author.mention}の接続時間\n"

        desc += f"`{self.convert_str_usertime(db.connect_time.get_value())}`"

        e = discord.Embed(description=desc)

        await ctx.send(embeds=[e])

    @commands.hybrid_command(name="接続時間リセット")
    async def reset(self, ctx: commands.Context):
        """コマンド送信者の接続時間をリセットする"""
        if not ctx.guild:
            return

        db = VC_Stats(id=ctx.author.id)
        db.server_id.set_value(ctx.guild.id)

        await db.delete()

        e = discord.Embed(
            description=f"{ctx.author.mention}の接続時間をリセットしました。",
            color=discord.Color.red(),
        )
        await ctx.send(embeds=[e])

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if (before.channel and after.channel) and (before.channel == after.channel):
            return

        guild = member.guild

        if after.channel:
            if not self.connect_time_cache.get(guild.id):
                self.connect_time_cache[guild.id] = {}

            if not self.connect_time_cache[guild.id].get(member.id):
                self.connect_time_cache[guild.id][member.id] = discord.utils.utcnow()
            else:
                self.connect_time_cache[guild.id][member.id] = discord.utils.utcnow()

        if before.channel:
            if self.connect_time_cache.get(guild.id):
                if cached_connect_time := self.connect_time_cache[guild.id].get(
                    member.id
                ):
                    db = VC_Stats(
                        id=member.id,
                    )
                    db.server_id.set_value(guild.id)
                    await db.fetch()
                    db.connect_time.value += (
                        discord.utils.utcnow() - cached_connect_time
                    ).total_seconds()

                    if db.is_none:
                        await db.insert()
                    else:
                        await db.update()


async def setup(bot):
    await bot.add_cog(VcStats(bot))
