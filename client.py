from importlib import import_module
from typing import Optional
from velum import GatewayBot, MessageCreateEvent
from os import listdir, path

from commands import Command


class Client(GatewayBot):
    def __init__(self, name: str, prefix: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._prefix = prefix
        self._commands: dict[str, Command] = {}
        self.subscribe(MessageCreateEvent, self.on_message)
        self.add_command(Command(self.help_command, "help"))

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            raise ValueError("No prefix has been registered")
        return self._prefix

    async def send(self, content: str):
        await self.rest.send_message(content, self.name)

    def add_command(self, command: Command):
        self._commands[command.name] = command

    def load_commands(self, directory: str):
        for file in listdir(directory):
            if path.isdir(file):
                self.load_commands(f"{directory}/{file}")
            else:
                if file.endswith("py"):
                    module = import_module(
                        f"{directory}/{file[:-3]}".replace("/", "."))
                    for obj in module.__dict__.values():
                        if isinstance(obj, Command):
                            self.add_command(obj)

    async def on_message(self, event: MessageCreateEvent):
        if event.author == self.name:
            return
        content = event.content[len(self.prefix):]
        command_name: str = ""
        args = None
        for i, char in enumerate(content):
            if char in [" ", "\n"]:
                i += 1
                args = content[i:] if len(content[i:]) > 0 else None
                break
            else:
                command_name += char
        if (command := self._commands.get(command_name, None)) is not None:
            try:
                await command.func(self, event, args)
            except Exception as e:
                await self.send(f"a fucky wucky has occured\n\n{e}")
                raise

    async def help_command(self, _client: GatewayBot, _event: MessageCreateEvent, args: Optional[str]):
        """A simple simple simple help command."""
        if args is None:
            longest = [len(name)
                       for name in self._commands.keys()]
            longest.sort(reverse=True)
            padding = longest[0] + 4
            return await self.send("```\n" + "\n".join(f"{name}:{' ' * (padding - len(name))}{cmd.desc}" for name, cmd in self._commands.items()) + "\n```")
        if (cmd := self._commands.get(args.split()[0])) is not None:
            await self.send(f"{cmd.name}\n\n{cmd.desc}")
        else:
            await self.send("Command not found")
