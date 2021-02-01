import re
from typing import List, Tuple

from cachetools import cached, TTLCache

from src.core.datasource import rcon_command

entity_list_pattern = re.compile(r"(\d+): (\w+):(\w+)")
mod_list_pattern = re.compile(r".*: (\w+) \((.+)\)")


@cached(cache=TTLCache(maxsize=1, ttl=60))
def get_players_online() -> List[str]:
    return (
        [y.strip() for y in x.split(":")[1].split(",")]
        if (x := rcon_command("list"))
        else []
    )


def get_entities() -> List[Tuple[str, str, str]]:
    return (
        entity_list_pattern.findall(x)
        if (x := rcon_command("forge entity list"))
        else []
    )


@cached(cache=TTLCache(maxsize=1, ttl=600))
def get_mods() -> List[Tuple[str, str]]:
    return mod_list_pattern.findall(x) if (x := rcon_command("forge mods")) else []
