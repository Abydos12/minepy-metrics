from prometheus_client.metrics_core import GaugeMetricFamily

from src.utils import get_player_names


def get_players_uuid_name_metric():
    g = GaugeMetricFamily(
        "mc_player_uuid", "Give player's name and uuid", labels=["uuid", "player"]
    )
    for player_uuid, player_name in get_player_names().items():
        g.add_metric([player_uuid, player_name], 1)
    return g
