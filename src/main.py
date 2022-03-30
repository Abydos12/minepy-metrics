import logging
import uvicorn
from mcrcon import MCRcon, MCRconException
from prometheus_client import REGISTRY, make_asgi_app

from src.collectors.rcon_collector import RconCollector
from src.config import RCON_ENABLED, FORGE_SERVER, RCON_HOST, RCON_PASSWORD, RCON_PORT
from src.core.metrics import (
    players_uuid_name,
    world_infos,
    player_data,
)
from src.core.player_stats import player_stats_metrics
from src.core.datasource import load_players
from src.tools.rcon_client import RconClient, rcon_connection

if RCON_ENABLED:
    try:
        with MCRcon(host=RCON_HOST, password=RCON_PASSWORD, port=RCON_PORT) as rcon:
            REGISTRY.register(RconCollector(rcon))
            if FORGE_SERVER:
                pass
    except (MCRconException, OSError) as e:
        logging.error(f"Connection to RCON failed: {e}")


class MinecraftCollector:
    def collect(self):

        yield players_uuid_name()
        yield world_infos()

        for player in load_players():

            for metric in player_data(player["uuid"], player["name"]).values():
                yield metric

            for metric in player_stats_metrics(player["uuid"], player["name"]).values():
                yield metric


REGISTRY.register(MinecraftCollector())

app = make_asgi_app()

if __name__ == "__main__":
    logging.info(f"Start on port [8000]")
    logging.info(f"RCON is [{'ENABLED' if RCON_ENABLED else 'DISABLED'}]")
    uvicorn.run(app, host="0.0.0.0", port=8000)
