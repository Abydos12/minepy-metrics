from mcrcon import MCRcon
from prometheus_client.metrics_core import GaugeMetricFamily

from src.core.datasource import load_players
from src.tools.rcon_client import RconClient, RconForgeClient


class Metrics:
    mc_player_entities_loaded = GaugeMetricFamily(
        "mc_player_entities_loaded",
        "Give entities loaded on forge server",
        labels=("mod", "entity"),
    )


class RconForgeCollector:
    rcon_client: RconForgeClient
    metrics = Metrics()

    def __init__(self, rcon: MCRcon):
        self.rcon_client = RconForgeClient(rcon)

    def collect(self):
        for count, mod, entity in self.rcon_client.get_entities():
            self.metrics.mc_player_entities_loaded.add_metric((mod, entity), int(count))
        yield self.metrics.mc_player_entities_loaded
