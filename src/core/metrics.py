from prometheus_client.metrics_core import GaugeMetricFamily, CounterMetricFamily

from src.core.datasource import load_players, load_level_data, load_player_data


def players_online():
    g = GaugeMetricFamily(
        name="mc_players_online",
        documentation="gives players online",
        labels=("player",),
    )
    for player in load_players():
        g.add_metric(labels=(player["name"],), value=1 if player["name"] in get_players_online() else 0)
    return g


def players_uuid_name():
    g = GaugeMetricFamily(
        "mc_player_uuid", "Give player's name and uuid", labels=("uuid", "player")
    )
    for player in load_players():
        g.add_metric((player["uuid"], player["name"]), 1)
    return g


def entities_loaded():
    g = GaugeMetricFamily(
        "mc_player_entities_loaded",
        "Give entities loaded on forge server",
        labels=("mod", "entity"),
    )
    for count, mod, entity in get_entities():
        g.add_metric((mod, entity), int(count))
    return g


def mods():
    g = GaugeMetricFamily(
        "mc_player_mods", "Give mods on forge server", labels=("mod", "version")
    )
    for mod, version in get_mods():
        g.add_metric((mod, version), 1)
    return g


def world_infos():
    g = GaugeMetricFamily(
        name="mc_world_infos",
        documentation="Give server info",
        labels=("version", "difficulty", "game_mode", "hardcore"),
    )
    if infos := load_level_data():
        g.add_metric(
            (
                infos["Data"]["Version"]["Name"].value,
                str(infos["Data"]["Difficulty"].value),
                str(infos["Data"]["GameType"].value),
                str(infos["Data"]["hardcore"].value),
            ),
            1,
        )
    return g


def player_data(uuid: str, name: str):
    metrics = {
        "foodLevel": GaugeMetricFamily(
            name="mc_player_food_level",
            documentation="Give food level",
            labels=["player"],
        ),
        "foodSaturationLevel": GaugeMetricFamily(
            name="mc_player_food_saturation_level",
            documentation="Give food saturation level",
            labels=["player"],
        ),
        "Health": GaugeMetricFamily(
            name="mc_player_health", documentation="Give health", labels=["player"]
        ),
        "Score": GaugeMetricFamily(
            name="mc_player_score", documentation="Give score", labels=["player"]
        ),
        "XpLevel": GaugeMetricFamily(
            name="mc_player_xp_level", documentation="Give xp level", labels=["player"]
        ),
        "XpTotal": CounterMetricFamily(
            name="mc_player_xp", documentation="Give xp total", labels=["player"]
        ),
    }
    data = load_player_data(uuid)
    if data:
        for key, metric in metrics.items():
            metric.add_metric(labels=[name], value=data[key].value)
    return metrics
