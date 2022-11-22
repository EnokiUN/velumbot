from asyncio import run

from client import Client

client = Client("Vuwuki", "!")

client.load_commands("cmds")
run(client.start())
