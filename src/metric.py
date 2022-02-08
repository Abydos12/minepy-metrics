from typing import Dict

from prometheus_client.metrics_core import Metric


class CustomCounter(Metric):
    def __init__(self, name: str, documentation: str, labels):
        super().__init__(name, documentation, "counter")

    def add_metric(self, labels: Dict[str, str], value):
        self.add_sample(self.name, labels, value)

    def clear_metrics(self):
        self.samples.clear()


class MetricsContainer:
    def __iter__(self):
        for d in dir(self):
            if not d.startswith("__"):
                yield self.__getattribute__(d)

    def metrics(self):
        return self.__iter__()


class PlayerStatsMetrics(MetricsContainer):
    mined = CustomCounter(
        name="mc_player_mined",
        documentation="The number of times the player mined an item",
        labels=("player", "mod", "item"),
    )
    broken = CustomCounter(
        name="mc_player_broken",
        documentation="The number of times the player broke an item",
        labels=("player", "mod", "item"),
    )
    crafted = CustomCounter(
        name="mc_player_crafted",
        documentation="The number of times the player crafted an item",
        labels=("player", "mod", "item"),
    )
    used = CustomCounter(
        name="mc_player_used",
        documentation="The number of times the player used an item",
        labels=("player", "mod", "item"),
    )
    picked_up = CustomCounter(
        name="mc_player_picked_up",
        documentation="The number of times the player picked up an item",
        labels=("player", "mod", "item"),
    )
    dropped = CustomCounter(
        name="mc_player_dropped",
        documentation="The number of times the player dropped an item",
        labels=("player", "mod", "item"),
    )
    killed = CustomCounter(
        name="mc_player_entity_killed",
        documentation="The number of times the player killed an entity",
        labels=("player", "mod", "entity"),
    )


if __name__ == "__main__":
    x = PlayerStatsMetrics()
    print()
