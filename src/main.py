import logging

from prometheus_client import start_http_server, REGISTRY
import time
import uvicorn
from prometheus_client import REGISTRY, make_asgi_app

from src import RCON_ENABLED
from src.core.player_stats import player_stats_metrics

logging.basicConfig(level=logging.INFO)

class MinecraftCollector(object):
    def collect(self):
        if RCON_ENABLED:
            yield players_online()

        yield players_uuid_name()
        yield world_infos()

        for player_uuid, player_name in load_player_names().items():

            for metric in player_data(player_uuid, player_name).values():
                yield metric

            for metric in player_stats_metrics(player_uuid, player_name).values():
                yield metric


REGISTRY.register(MinecraftCollector())

app = make_asgi_app()


if __name__ == "__main__":
    print(f"Start on port [8000]")
    print(f"RCON is [{'ENABLED' if RCON_ENABLED else 'DISABLED'}]")
    uvicorn.run(app, port=8000, log_level="info")
