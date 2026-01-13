"""
discordbotlist.client - Client module for discordbotlist.py
Copyright (c) 2021-2026 Rezn1r
"""
try:
    from discord import Client as DiscordClient # type: ignore
    from discord import AutoShardedClient # type: ignore
except ImportError:
    raise RuntimeError(
        "You must install either `discord.py` or `py-cord`. "
        "Use `pip install discordbotlist-py[discord]` or "
        "`pip install discordbotlist-py[pycord]`"
    )

try:
    import importlib.metadata as meta
    IS_PYCORD = bool(meta.version("py-cord"))
except Exception:
    IS_PYCORD = False

import aiohttp

from .constants import API_BASE_URL
import asyncio
from typing import TypedDict


class AppCommandPayload(TypedDict):
    name: str
    description: str
    type: int


class DblClient:
    def __init__(self, token: str, client: DiscordClient) -> None:
        self.token = token
        self.client = client
        self._post_task: asyncio.Task | None = None
        self._listeners: dict[str, list] = {}

    async def post_status(self) -> None:
        """Posts the current server count to DiscordBotList."""
        if self.client.user is None:
            raise ValueError("Client is not logged in.")

        if not self.client.intents.guilds:
            raise ValueError(
                "Guilds intent is disabled. Enable it to post server count."
            )

        if not self.client.intents.members:
            raise ValueError(
                "Members intent is disabled. Enable it to post accurate server count."
            )

        bot_id = self.client.user.id
        shard_id = (
            self.client.shard_id if isinstance(self.client, AutoShardedClient) else None
        )

        if shard_id is not None:
            payload = {
                "voice_connections": len(self.client.voice_clients),
                "guilds": len(self.client.guilds),
                "users": sum(g.member_count or 0 for g in self.client.guilds),
                "shard_id": shard_id,
            }
        else:
            payload = {
                "voice_connections": len(self.client.voice_clients),
                "guilds": len(self.client.guilds),
                "users": sum(g.member_count or 0 for g in self.client.guilds),
            }

        headers = {"Authorization": self.token}
        url = f"{API_BASE_URL}/bots/{bot_id}/stats"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        f"Failed to post stats: {resp.status} - {await resp.text()}"
                    )

        # Dispatch the dbl_updated event
        await self._dispatch("on_dbl_updated", payload)

    async def _posting_loop(self, interval: int) -> None:
        try:
            while True:
                try:
                    await self.post_status()
                except Exception as e:
                    print(f"Error posting status: {e}")

                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            pass

    def start_posting(self, interval: int = 3600) -> None:
        """Start the background posting loop (non-blocking)."""
        if self._post_task is not None and not self._post_task.done():
            return  # already running

        self._post_task = asyncio.create_task(
            self._posting_loop(interval),
            name="dbl-posting-loop",
        )

    async def stop_posting(self) -> None:
        """Stop the background posting loop."""
        if self._post_task is not None:
            self._post_task.cancel()
            try:
                await self._post_task
            except asyncio.CancelledError:
                pass
            self._post_task = None

    def event(self, func):
        """Decorator to register an event listener. Use like @dbl_client.event"""
        event_name = func.__name__
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(func)
        return func

    async def _dispatch(self, event_name: str, *args, **kwargs) -> None:
        """Internal method to dispatch events to all registered listeners."""
        if event_name not in self._listeners:
            return

        for listener in self._listeners[event_name]:
            asyncio.create_task(listener(*args, **kwargs))

    async def post_command(self, commands: list[AppCommandPayload]) -> None:
        """Posts the bot's commands to DiscordBotList."""

        headers = {"Authorization": self.token}
        bot_id = self.client.user.id if self.client.user else None
        if bot_id is None:
            raise ValueError("Client is not logged in.")

        url = f"{API_BASE_URL}/bots/{bot_id}/commands"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=commands, headers=headers) as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        f"Failed to post commands: {resp.status} - {await resp.text()}"
                    )

        # Dispatch the dbl_commands_updated event
        await self._dispatch("on_dbl_commands_updated", commands)
