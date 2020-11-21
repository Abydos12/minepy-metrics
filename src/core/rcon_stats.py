from prometheus_client.metrics_core import GaugeMetricFamily

from src.utils import get_player_names, rcon_command


def get_players_online():
    return x.split(":")[1].split(",") if (x := rcon_command("list")) else []


def get_players_online_metric():
    g = GaugeMetricFamily(
        name="mc_players_online",
        documentation="gives players online",
        labels=["player"],
    )
    online_players = get_players_online()
    for player in get_player_names().values():
        g.add_metric(
            labels=[player], value=1
        ) if player in online_players else g.add_metric(labels=[player], value=0)
    return g
