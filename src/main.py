import logging

from prometheus_client import start_http_server, REGISTRY
import time

from src import RCON_ENABLED
from src.core.nbt_stats import setup_player_data_metrics
from src.core.player_stats import setup_player_stats_metrics
from src.core.rcon_stats import get_players_online_metric
from src.core.server_stats import get_players_uuid_name_metric, get_server_infos_metric
from src.utils import get_player_names

logging.basicConfig(level=logging.INFO)

class MinecraftCollector(object):
    def collect(self):

        if RCON_ENABLED:
            yield get_players_online_metric()

        yield get_players_uuid_name_metric()
        yield get_server_infos_metric()

        for player_uuid, player_name in get_player_names().items():

            for metric in setup_player_data_metrics(player_uuid, player_name).values():
                yield metric

            for metric in setup_player_stats_metrics(player_uuid, player_name).values():
                yield metric


REGISTRY.register(MinecraftCollector())

if __name__ == "__main__":
    start_http_server(port=8000)
    logging.info(f"Start on port [8000]")
    logging.info(f"RCON is [{'ENABLED' if RCON_ENABLED else 'DISABLED'}]")
    while True:
        time.sleep(1)
