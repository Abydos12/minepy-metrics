import json
import logging
from typing import Dict

from cachetools.func import ttl_cache
from mcrcon import MCRcon, MCRconException
from nbt import nbt

from src import ROOT_PATH, RCON_HOST, RCON_PASSWORD, RCON_PORT


@ttl_cache(maxsize=1, ttl=60)
def get_player_names() -> Dict[str, str]:
    try:
        with open(f"{ROOT_PATH}/usernamecache.json", "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.error(f"File [{ROOT_PATH}/usernamecache.json] not found")
        return {}


def get_player_stats(uuid: str) -> Dict[str, int]:
    try:
        with open(f"{ROOT_PATH}/world/stats/{uuid}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.error(f"File [{ROOT_PATH}/world/stats/{uuid}.json] not found")
        return {}


def get_player_data(uuid: str):
    try:
        return nbt.NBTFile(f"{ROOT_PATH}/world/playerdata/{uuid}.dat", "rb")
    except FileNotFoundError as e:
        logging.error(f"File [{ROOT_PATH}/world/playerdata/{uuid}.dat] not found")


def rcon_command(command: str):
    try:
        with MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT) as rcon:
            return rcon.command(f"/{command}")
    except MCRconException as e:
        logging.error(f"Connection to RCON failed: {e}")


if __name__ == "__main__":
    logging.info(get_player_names())
