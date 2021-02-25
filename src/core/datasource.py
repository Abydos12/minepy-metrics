import json
import logging
from typing import Dict

from cachetools import cached, TTLCache
from cachetools.func import ttl_cache
from mcrcon import MCRcon, MCRconException
from nbt import nbt

from src import ROOT_PATH, RCON_HOST, RCON_PASSWORD, RCON_PORT


def rcon_command(command: str):
    try:
        with MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT) as rcon:
            return rcon.command(f"/{command}")
    except (MCRconException, OSError) as e:
        logging.error(f"Connection to RCON failed: {e}")


@ttl_cache(maxsize=1, ttl=60)
def load_player_names() -> Dict[str, str]:
    try:
        with open(f"{ROOT_PATH}/usernamecache.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File [{ROOT_PATH}/usernamecache.json] not found")
        return {}


def load_player_stats(uuid: str):
    try:
        with open(f"{ROOT_PATH}/world/stats/{uuid}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File [{ROOT_PATH}/world/stats/{uuid}.json] not found")
        return {}


def load_player_data(uuid: str):
    try:
        return nbt.NBTFile(f"{ROOT_PATH}/world/playerdata/{uuid}.dat", "rb")
    except FileNotFoundError as e:
        logging.error(f"File [{ROOT_PATH}/world/playerdata/{uuid}.dat] not found")


def load_level_data():
    try:
        return nbt.NBTFile(f"{ROOT_PATH}/world/level.dat", "rb")
    except FileNotFoundError:
        logging.error(f"File [{ROOT_PATH}/world/level.dat] not found")


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
