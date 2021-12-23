import logging
from typing import Dict, List

from cachetools import cached, TTLCache

from src.config import ROOT_PATH
from src.tools.file_cache import JsonFileCache, NbtFileCache

json_file_cache = JsonFileCache()
nbt_file_cache = NbtFileCache()


def load_players() -> List[Dict[str, str]]:
    return json_file_cache[f"{ROOT_PATH}/usercache.json"] or []


def load_player_stats(uuid: str):
    return json_file_cache[f"{ROOT_PATH}/world/stats/{uuid}.json"] or {}


def load_player_data(uuid: str):
    return nbt_file_cache[f"{ROOT_PATH}/world/playerdata/{uuid}.dat"]


def load_level_data():
    return nbt_file_cache[f"{ROOT_PATH}/world/level.dat"]


@cached(cache=TTLCache(maxsize=1, ttl=600))
def get_server_properties():
    try:
        with open(f"{ROOT_PATH}/server.properties", "r") as f:
            properties = {}
            for line in f:
                if "=" in line:
                    key, value = line.split("=")
                    properties[key] = value
    except FileNotFoundError:
        logging.error(f"File [{ROOT_PATH}/server.properties] not found")
        return {}
    else:
        return properties
