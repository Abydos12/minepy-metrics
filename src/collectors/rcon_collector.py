from mcrcon import MCRcon
from prometheus_client.metrics_core import GaugeMetricFamily

from src.core.datasource import load_players
from src.tools.rcon_client import RconClient


class Metrics:
    players_online = GaugeMetricFamily(
        name="mc_players_online",
        documentation="gives players online",
        labels=("player",),
    )


class RconCollector:
    rcon_client: RconClient
    metrics = Metrics()

    def __init__(self, rcon: MCRcon):
        self.rcon_client = RconClient(rcon)

    def collect(self):
        for player in load_players():
            self.metrics.players_online.add_metric(
                labels=(player["name"],),
                value=1
                if player["name"] in self.rcon_client.get_players_online()
                else 0,
            )
        yield self.metrics.players_online
