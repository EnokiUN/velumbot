from typing import Optional
from velum import MessageCreateEvent
from client import Client
from commands import command


@command()
async def foo(client: Client, event: MessageCreateEvent, args: Optional[str]):
    """Replies with bar"""
    await client.send("bar")
