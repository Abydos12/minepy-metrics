import logging
import re
from typing import List, Tuple

from cachetools import TTLCache, cached
from mcrcon import MCRcon, MCRconException

from src.config import RCON_ENABLED, RCON_HOST, RCON_PASSWORD, RCON_PORT


class RconClient:
    rcon_client: MCRcon

    def __init__(self):
        if RCON_ENABLED:
            try:
                rcon = MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT)
            except (MCRconException, OSError) as e:
                logging.error(f"Connection to RCON failed: {e}")
            else:
                self.rcon_client = rcon
                self.rcon_client.connect()

    def __del__(self):
        if self.rcon_client is not None:
            self.rcon_client.disconnect()

    def command(self, command: str):
        if len(command) > 0:
            return self.rcon_client.command("/" + command)

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def get_players_online(self) -> List[str]:
        return (
            [y.strip() for y in x.split(":")[1].split(",")]
            if (x := self.command("list"))
            else []
        )


entity_list_pattern = re.compile(r"(\d+): (\w+):(\w+)")
mod_list_pattern = re.compile(r".*: (\w+) \((.+)\)")


class ForgeRcon:
    rcon_client: RconClient

    def __init__(self, rcon_client: RconClient):
        self.rcon_client = rcon_client

    def get_entities(self) -> List[Tuple[str, str, str]]:
        return (
            entity_list_pattern.findall(x)
            if (x := self.rcon_client.command("forge entity list"))
            else []
        )

    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def get_mods(self) -> List[Tuple[str, str]]:
        return mod_list_pattern.findall(x) if (x := self.rcon_client.command("forge mods")) else []
