import logging
import uvicorn
from prometheus_client import REGISTRY, make_asgi_app

from src import RCON_ENABLED, FORGE_SERVER
from src.core.metrics import (
    players_online,
    players_uuid_name,
    world_infos,
    player_data,
    entities_loaded,
    mods,
)
from src.core.player_stats import player_stats_metrics
from src.core.datasource import load_players


class MinecraftCollector:
    def collect(self):
        if RCON_ENABLED:
            yield players_online()
            if FORGE_SERVER:
                yield entities_loaded()
                yield mods()

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
