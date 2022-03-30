import contextlib
import logging
import re
from typing import List, Tuple

from cachetools import TTLCache, cached
from mcrcon import MCRcon, MCRconException

from ..config import RCON_ENABLED, RCON_HOST, RCON_PASSWORD, RCON_PORT


@contextlib.contextmanager
def rcon_connection():
    rcon = MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT)
    try:
        rcon.connect()
        yield rcon

        raise e
    finally:
        rcon.disconnect()


class BaseRconClient:
    rcon: MCRcon

    def __init__(self, rcon: MCRcon):
        self.rcon = rcon

    def command(self, command: str):
        if len(command) > 0:
            return self.rcon.command("/" + command)


class RconClient(BaseRconClient):
    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def get_players_online(self) -> List[str]:
        return (
            [y.strip() for y in x.split(":")[1].split(",")]
            if (x := self.command("list"))
            else []
        )


entity_list_pattern = re.compile(r"(\d+): (\w+):(\w+)")
mod_list_pattern = re.compile(r".*: (\w+) \((.+)\)")


class RconForgeClient(BaseRconClient):
    def get_entities(self) -> List[Tuple[str, str, str]]:
        return (
            entity_list_pattern.findall(x)
            if (x := self.rcon.command("forge entity list"))
            else []
        )

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def get_mods(self) -> List[Tuple[str, str]]:
        return (
            mod_list_pattern.findall(x)
            if (x := self.rcon.command("forge mods"))
            else []
        )
