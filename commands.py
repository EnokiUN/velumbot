from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional

from velum import MessageCreateEvent

if TYPE_CHECKING:
    from client import Client

    CommandFunc = Callable[
        [Client, MessageCreateEvent, Optional[str]], Coroutine[Any, Any, Any]
    ]


class Command:
    def __init__(
        self,
        func: CommandFunc,
        name: Optional[str] = None,
        desc: Optional[str] = None,
    ):
        self.func = func
        self.name = name or func.__name__
        self.desc = desc


def command(name: Optional[str] = None, desc: Optional[str] = None):
    def inner(func: CommandFunc):
        return Command(func, name, desc)

    return inner
