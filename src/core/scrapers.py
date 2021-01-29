from typing import List

from cachetools import cached, TTLCache

from src.core.datasource import rcon_command


@cached(cache=TTLCache(maxsize=1, ttl=60))
def get_players_online() -> List[str]:
    return (
        [y.strip() for y in x.split(":")[1].split(",")]
        if (x := rcon_command("list"))
        else []
    )
