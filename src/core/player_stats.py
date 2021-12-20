import logging
import re
from typing import Dict

from cachetools import cached
from prometheus_client.metrics_core import CounterMetricFamily

from src.core.datasource import load_player_stats

pattern = re.compile(r"(?<!^)(?=[A-Z])")


@cached(cache={})
def camel_to_snake(txt: str):
    return pattern.sub("_", txt).lower()


INTERACTIONS = {
    "open_barrel": "barrel",
    "trigger_trapped_chest": "trapped_chest",
    "talked_to_villager": "villager",
    "open_shulker_box": "shulker_box",
    "bell_ring": "bell",
    "eat_cake_slice": "cake_slice",
    "open_chest": "chest",
    "inspect_dispenser": "dispenser",
    "inspect_dropper": "dropper",
    "open_enderchest": "enderchest",
    "inspect_hopper": "hopper",
}

IGNORED = {"drop"}

INTERACTIONS_OLD = {
    "open_barrel": "barrel",
    "trapped_chest_triggered": "trapped_chest",
    "talked_to_villager": "villager",
    "open_shulker_box": "shulker_box",
    "bell_ring": "bell",
    "cake_slices_eaten": "cake_slice",
    "chest_opened": "chest",
    "dispenser_inspected": "dispenser",
    "dropper_inspected": "dropper",
    "enderchest_opened": "enderchest",
    "hopper_inspected": "hopper",
}


def _player_stats_metrics() -> Dict[str, CounterMetricFamily]:
    return {
        "mined": CounterMetricFamily(
            name="mc_player_mined",
            documentation="The number of times the player mined an item",
            labels=("player", "mod", "item"),
        ),
        "broken": CounterMetricFamily(
            name="mc_player_broken",
            documentation="The number of times the player broke an item",
            labels=("player", "mod", "item"),
        ),
        "crafted": CounterMetricFamily(
            name="mc_player_crafted",
            documentation="The number of times the player crafted an item",
            labels=("player", "mod", "item"),
        ),
        "used": CounterMetricFamily(
            name="mc_player_used",
            documentation="The number of times the player used an item",
            labels=("player", "mod", "item"),
        ),
        "picked_up": CounterMetricFamily(
            name="mc_player_picked_up",
            documentation="The number of times the player picked up an item",
            labels=("player", "mod", "item"),
        ),
        "dropped": CounterMetricFamily(
            name="mc_player_dropped",
            documentation="The number of times the player dropped an item",
            labels=("player", "mod", "item"),
        ),
        "killed": CounterMetricFamily(
            name="mc_player_entity_killed",
            documentation="The number of times the player killed an entity",
            labels=("player", "mod", "entity"),
        ),
        "mob_kills": CounterMetricFamily(
            name="mc_player_mob_kills",
            documentation="The number of mobs the player killed",
            labels=("player",),
        ),
        "killed_by": CounterMetricFamily(
            name="mc_player_killed_by",
            documentation="The number of times the player being killed by entities",
            labels=("player", "mod", "entity"),
        ),
        "animals_bred": CounterMetricFamily(
            name="mc_player_animals_bred",
            documentation="The number of times the player bred two mobs",
            labels=("player",),
        ),
        "clean": CounterMetricFamily(
            name="mc_player_item_cleaned",
            documentation="	The number of item washed with a cauldron",
            labels=("player", "item"),
        ),
        "interact": CounterMetricFamily(
            name="mc_player_interacted",
            documentation="The number of times the player interact with something (barrel, chest, table, villager, etc...)",
            labels=("player", "with"),
        ),
        "fill_cauldron": CounterMetricFamily(
            name="mc_player_cauldron_filled",
            documentation="The number of times the player filled cauldrons with water buckets",
            labels=("player",),
        ),
        "damage_absorbed": CounterMetricFamily(
            name="mc_player_damage_absorbed",
            documentation="The amount of damage the player has absorbed in tenths of 1",
            labels=("player",),
        ),
        "damage_blocked_by_shield": CounterMetricFamily(
            name="mc_player_damage_blocked_by_shield",
            documentation="The amount of damage the player has blocked with a shield in tenths of 1",
            labels=("player",),
        ),
        "damage_dealt": CounterMetricFamily(
            name="mc_player_damage_dealt",
            documentation="The amount of damage the player has dealt in tenths 1. Includes only melee attacks",
            labels=("player",),
        ),
        "damage_dealt_absorbed": CounterMetricFamily(
            name="mc_player_damage_dealt_absorbed",
            documentation="The amount of damage the player has dealt that were absorbed, in tenths of 1",
            labels=("player",),
        ),
        "damage_dealt_resisted": CounterMetricFamily(
            name="mc_player_damage_dealt_resisted",
            documentation="The amount of damage the player has dealt that were resisted, in tenths of 1",
            labels=("player",),
        ),
        "damage_resisted": CounterMetricFamily(
            name="mc_player_damage_resisted",
            documentation="The amount of damage the player has resisted in tenths of 1",
            labels=("player",),
        ),
        "damage_taken": CounterMetricFamily(
            name="mc_player_damage_taken",
            documentation="The amount of damage the player has taken in tenths of 1",
            labels=("player",),
        ),
        "distance": CounterMetricFamily(
            name="mc_player_distance",
            documentation="The total distance traveled (walk, fall, swim, pig, etc...)",
            labels=("player", "by"),
        ),
        "fish_caught": CounterMetricFamily(
            name="mc_player_fish_caught",
            documentation="The number of fish caught",
            labels=("player",),
        ),
        "leave_game": CounterMetricFamily(
            name="mc_player_leave_game",
            documentation="The number of times 'Save and quit to title' has been clicked",
            labels=("player",),
        ),
        "enchant_item": CounterMetricFamily(
            name="mc_player_item_enchanted",
            documentation="The number of items enchanted",
            labels=("player",),
        ),
        "jump": CounterMetricFamily(
            name="mc_player_jump",
            documentation="The total number of jumps performed",
            labels=("player",),
        ),
        "play_record": CounterMetricFamily(
            name="mc_player_record_played",
            documentation="The number of music discs played on a jukebox",
            labels=("player",),
        ),
        "play_noteblock": CounterMetricFamily(
            name="mc_player_noteblock_played",
            documentation="The number of note blocks hit",
            labels=("player",),
        ),
        "tune_noteblock": CounterMetricFamily(
            name="mc_player_noteblock_tuned",
            documentation="The number of times interacted with note blocks",
            labels=("player",),
        ),
        "deaths": CounterMetricFamily(
            name="mc_player_deaths",
            documentation="The number of times the player died",
            labels=("player",),
        ),
        "pot_flower": CounterMetricFamily(
            name="mc_player_plants_potted",
            documentation="The number of plants potted onto flower pots",
            labels=("player",),
        ),
        "player_kills": CounterMetricFamily(
            name="mc_player_killed_players",
            documentation="The number of players the player killed (on PvP servers). Indirect kills do not count",
            labels=("player",),
        ),
        "raid_trigger": CounterMetricFamily(
            name="mc_player_triggered_raid",
            documentation="The number of times the player has triggered a Raid",
            labels=("player",),
        ),
        "raid_win": CounterMetricFamily(
            name="mc_player_won_raid",
            documentation="The number of times the player has won a Raid",
            labels=("player",),
        ),
        "target_hit": CounterMetricFamily(
            name="mc_player_hit_target",
            documentation="The number of times the player has shot a target block",
            labels=("player",),
        ),
        "time": CounterMetricFamily(
            name="mc_player_time_spend",
            documentation="The total amount of time in sec [since death, since rest, played, sneak])",
            labels=("player", "action"),
        ),
        "sleep_in_bed": CounterMetricFamily(
            name="mc_player_slept_in_bed",
            documentation="The number of times the player has slept in a bed",
            labels=("player",),
        ),
        "traded_with_villager": CounterMetricFamily(
            name="mc_player_traded_with_villager",
            documentation="The number of times traded with villagers",
            labels=("player",),
        ),
        "use_cauldron": CounterMetricFamily(
            name="mc_player_used_cauldron",
            documentation="The number of times the player took water from cauldrons with glass bottles",
            labels=("player",),
        ),
    }


def player_stats_metrics(uuid: str, name: str) -> Dict:
    player_stats = load_player_stats(uuid)
    return (
        fill_after_1_13(name, player_stats)
        if player_stats.get("stats")
        else fill_before_1_13(name, player_stats)
    )


def fill_after_1_13(name: str, player_stats: Dict[str, Dict[str, Dict[str, int]]]):
    metrics = _player_stats_metrics()
    player_stats = player_stats["stats"]

    for category, sub in player_stats.items():
        category = category.split(":")[1]

        for key, value in sub.items():
            mod, item = key.split(":")
            if category == "custom":
                if item.endswith("_one_cm"):
                    metrics["distance"].add_metric(
                        (name, item[: -len("_one_cm")]), value
                    )
                elif item.startswith("clean_"):
                    metrics["clean"].add_metric((name, item[len("clean_") :]), value)
                elif item.startswith("time_since_"):
                    metrics["time"].add_metric(
                        (name, item[len("time_") :]), value / 20 if value else 0
                    )
                elif item == "play_one_minute":
                    metrics["time"].add_metric(
                        (name, "played"), value / 20 if value else 0
                    )
                elif item == "sneak_time":
                    metrics["time"].add_metric(
                        (name, "sneak"), value / 20 if value else 0
                    )
                elif item in INTERACTIONS.keys():
                    metrics["interact"].add_metric((name, INTERACTIONS[item]), value)
                elif item.startswith("interact_with_"):
                    metrics["interact"].add_metric(
                        (name, item[len("interact_with_") :]), value
                    )
                elif item in IGNORED:
                    continue
                elif item in metrics:
                    metrics[item].add_metric((name,), value)
                else:
                    logging.error(f"metric [{item}] not supported")
            else:
                metrics[category].add_metric((name, mod, item), value)

    return metrics


def fill_before_1_13(name: str, player_stats):
    metrics = _player_stats_metrics()
    for keys, value in player_stats.items():
        keys = keys.split(".")[1:]  # ignore "stat"
        if len(keys) == 3:
            key, mod, item = keys
        elif len(keys) == 2:
            key, mod, item = keys[0], "minecraft", keys[1]
        elif len(keys) > 3:
            key, mod, item = keys[0], keys[1], ".".join(keys[2:])
        else:
            key, mod, item = keys[0], "", ""
        key = camel_to_snake(key)

        if key.endswith("_one_cm"):
            metrics["distance"].add_metric((name, key[: -len("OneCm")]), value)
        elif key.startswith("time_since_"):
            metrics["time"].add_metric(
                (name, key[len("time_since_") :]), value / 20 if value else 0
            )
        elif "play_one_minute" == key:
            metrics["time"].add_metric((name, "played"), value / 20 if value else 0)
        elif "sneak_time" == key:
            metrics["time"].add_metric((name, "sneak"), value / 20 if value else 0)
        elif key in INTERACTIONS_OLD.keys():
            metrics["interact"].add_metric((name, INTERACTIONS_OLD[key]), value)
        elif key.endswith("_interaction"):
            metrics["interact"].add_metric((name, item[: -len("_interaction")]), value)
        elif "mine_block" == key:
            metrics["mined"].add_metric((name, mod, item), value)
        elif "craft_item" == key:
            metrics["crafted"].add_metric((name, mod, item), value)
        elif "use_item" == key:
            metrics["used"].add_metric((name, mod, item), value)
        elif "pickup" == key:
            metrics["picked_up"].add_metric((name, mod, item), value)
        elif "drop" == key and mod and item:  # ignore drop total
            metrics["dropped"].add_metric((name, mod, item), value)
        elif "kill_entity" == key:
            metrics["killed"].add_metric((name, mod, item), value)
        elif "entity_killed_by" == key:
            metrics["killed_by"].add_metric((name, mod, item), value)
        elif "item_enchanted" == key:
            metrics["enchant_item"].add_metric((name,), value)
        elif "record_played" == key:
            metrics["play_record"].add_metric((name,), value)
        elif "flower_potted" == key:
            metrics["pot_flower"].add_metric((name,), value)

        elif key in IGNORED:
            continue
        else:
            try:
                metrics[key].add_metric((name,), value)
            except KeyError:
                logging.error(f"Unsupported keys {keys} for stats player")
    return metrics
