from prometheus_client.metrics_core import GaugeMetricFamily, SummaryMetricFamily

from src.utils import get_player_names, get_game_infos


def get_players_uuid_name_metric():
    g = GaugeMetricFamily(
        "mc_player_uuid", "Give player's name and uuid", labels=["uuid", "player"]
    )
    for player_uuid, player_name in get_player_names().items():
        g.add_metric([player_uuid, player_name], 1)
    return g


def get_server_infos_metric():
    g = GaugeMetricFamily(name="mc_server_info", documentation="Give server info", labels=["version", "difficulty", "game_mode"])
    infos = get_game_infos()
    if infos:
        g.add_metric(infos.values(), 1)

    return g
