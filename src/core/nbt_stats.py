from prometheus_client.metrics_core import GaugeMetricFamily, CounterMetricFamily

from src.utils import get_player_data


def generate_player_data_metrics():
    return {
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


def setup_player_data_metrics(uuid: str, name: str):
    player_data = get_player_data(uuid)
    player_data_metrics = generate_player_data_metrics()
    if player_data:
        for key, metric in player_data_metrics.items():
            metric.add_metric(labels=[name], value=player_data[key].value)

    return player_data_metrics
