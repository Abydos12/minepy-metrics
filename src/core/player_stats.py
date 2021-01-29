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

IGNORED = {"drop", "mob_kills"}

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
        # "clean_armor": CounterMetricFamily(
        #     name="mc_player_armor_cleaned",
        #     documentation="	The number of dyed leather armors washed with a cauldron",
        #     labels=("player",),
        # ),
        # "clean_banner": CounterMetricFamily(
        #     name="mc_player_banners_cleaned",
        #     documentation="The number of banner patterns washed with a cauldron",
        #     labels=("player",),
        # ),
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
        # "open_barrel": CounterMetricFamily(
        #     name="mc_player_barrels_open",
        #     documentation="The number of times the player has opened a Barrel",
        #     labels=("player",),
        # ),
        # "bell_ring": CounterMetricFamily(
        #     name="mc_player_bells_rung",
        #     documentation="The number of times the player has rung a Bell",
        #     labels=("player",),
        # ),
        # "eat_cake_slice": CounterMetricFamily(
        #     name="mc_player_cake_slices_eaten",
        #     documentation="The number of cake slices eaten",
        #     labels=("player",),
        # ),
        "fill_cauldron": CounterMetricFamily(
            name="mc_player_cauldron_filled",
            documentation="The number of times the player filled cauldrons with water buckets",
            labels=("player",),
        ),
        # "open_chest": CounterMetricFamily(
        #     name="mc_player_chests_opened",
        #     documentation="The number of times the player opened chests.",
        #     labels=("player",),
        # ),
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
        # "inspect_dispenser": CounterMetricFamily(
        #     name="mc_player_inspect_dispenser",
        #     documentation="The number of times interacted with dispensers",
        #     labels=("player",),
        # ),
        # "climb_one_cm": CounterMetricFamily(
        #     name="mc_player_climb",
        #     documentation="The total distance traveled up ladders or vines",
        #     labels=("player",),
        # ),
        # "crouch_one_cm": CounterMetricFamily(
        #     name="mc_player_crouch",
        #     documentation="The total distance walked while sneaking",
        #     labels=("player",),
        # ),
        # "fall_one_cm": CounterMetricFamily(
        #     name="mc_player_fall",
        #     documentation="The total distance fallen, excluding jumping. If the player falls more than one block, the entire jump is counted",
        #     labels=("player",),
        # ),
        # "fly_one_cm": CounterMetricFamily(
        #     name="mc_player_fly",
        #     documentation="Distance traveled upwards and forwards at the same time, while more than one block above the ground",
        #     labels=("player",),
        # ),
        # "sprint_one_cm": CounterMetricFamily(
        #     name="mc_player_sprint",
        #     documentation="The total distance sprinted",
        #     labels=("player",),
        # ),
        # "swim_one_cm": CounterMetricFamily(
        #     name="mc_player_swim",
        #     documentation="The total distance covered with sprint-swimming",
        #     labels=("player",),
        # ),
        # "walk_one_cm": CounterMetricFamily(
        #     name="mc_player_walk",
        #     documentation="The total distance walked",
        #     labels=("player",),
        # ),
        # "walk_on_water_one_cm": CounterMetricFamily(
        #     name="mc_player_walk_on_water",
        #     documentation="The distance covered while bobbing up and down over water",
        #     labels=("player",),
        # ),
        # "walk_under_water_one_cm": CounterMetricFamily(
        #     name="mc_player_walk_under_water",
        #     documentation="The total distance you have walked underwater",
        #     labels=("player",),
        # ),
        # "boat_one_cm": CounterMetricFamily(
        #     name="mc_player_boat",
        #     documentation="The total distance traveled by boats",
        #     labels=("player",),
        # ),
        # "aviate_one_cm": CounterMetricFamily(
        #     name="mc_player_aviate",
        #     documentation="The total distance traveled by elytra",
        #     labels=("player",),
        # ),
        # "horse_one_cm": CounterMetricFamily(
        #     name="mc_player_horse",
        #     documentation="The total distance traveled by horses",
        #     labels=("player",),
        # ),
        # "minecart_one_cm": CounterMetricFamily(
        #     name="mc_player_minecart",
        #     documentation="The total distance traveled by minecarts",
        #     labels=("player",),
        # ),
        # "pig_one_cm": CounterMetricFamily(
        #     name="mc_player_pig",
        #     documentation="The total distance traveled by pigs via saddles",
        #     labels=("player",),
        # ),
        # "strider_one_cm": CounterMetricFamily(
        #     name="mc_player_strider",
        #     documentation="The total distance traveled by striders via saddles",
        #     labels=("player",),
        # ),
        "distance": CounterMetricFamily(
            name="mc_player_distance",
            documentation="The total distance traveled (walk, fall, swim, pig, etc...)",
            labels=("player", "by"),
        ),
        # "inspect_dropper": CounterMetricFamily(
        #     name="mc_player_inspect_dropper",
        #     documentation="The number of times interacted with droppers",
        #     labels=("player",),
        # ),
        # "open_enderchest": CounterMetricFamily(
        #     name="mc_player_enderchest_opened",
        #     documentation="The number of times the player opened ender chests",
        #     labels=("player",),
        # ),
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
        # "inspect_hopper": CounterMetricFamily(
        #     name="mc_player_inspect_hopper",
        #     documentation="The number of times interacted with hoppers",
        #     labels=("player",),
        # ),
        # "interact_with_anvil": CounterMetricFamily(
        #     name="mc_player_anvil_interaction",
        #     documentation="The number of times interacted with anvils",
        #     labels=("player",),
        # ),
        # "interact_with_beacon": CounterMetricFamily(
        #     name="mc_player_beacon_interaction",
        #     documentation="The number of times interacted with beacons",
        #     labels=("player",),
        # ),
        # "interact_with_blast_furnace": CounterMetricFamily(
        #     name="mc_player_blast_furnace_interaction",
        #     documentation="The number of times interacted with Blast Furnaces",
        #     labels=("player",),
        # ),
        # "interact_with_brewingstand": CounterMetricFamily(
        #     name="mc_player_brewingstand_interaction",
        #     documentation="The number of times interacted with brewing stands",
        #     labels=("player",),
        # ),
        # "interact_with_campfire": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Campfires",
        #     labels=("player",),
        # ),
        # "interact_with_cartography_table": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Cartography Tables",
        #     labels=("player",),
        # ),
        # "interact_with_crafting_table": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with crafting tables",
        #     labels=("player",),
        # ),
        # "interact_with_furnace": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with furnaces",
        #     labels=("player",),
        # ),
        # "interact_with_gridstone": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Grindstones",
        #     labels=("player",),
        # ),
        # "interact_with_lectern": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Lecterns",
        #     labels=("player",),
        # ),
        # "interact_with_loom": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Looms",
        #     labels=("player",),
        # ),
        # "interact_with_smithing_table": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Smithing Tables",
        #     labels=("player",),
        # ),
        # "interact_with_smoker": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Smokers",
        #     labels=("player",),
        # ),
        # "interact_with_stonecutter": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with Stonecutters",
        #     labels=("player",),
        # ),
        # "drop": CounterMetricFamily(
        #     name="mc_player_drop",
        #     documentation="The number of items dropped. This does not include items dropped upon death. If a group of items are dropped together, eg a stack of 64, it only counts as 1",
        #     labels=("player",),
        # ),
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
        # "mob_kills": CounterMetricFamily(
        #     name="mc_player_mob_killed",
        #     documentation="The number of mobs the player killed",
        #     labels=("player",),
        # ),
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
        # "clean_shulker_box": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times the player has washed a Shulker Box with a cauldron",
        #     labels=("player",),
        # ),
        # "open_shulker_box": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times the player has opened a Shulker Box",
        #     labels=("player",),
        # ),
        # "sneak_time": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The time the player has held down the sneak button",
        #     labels=("player",),
        # ),
        # "talked_to_villager": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times interacted with villagers (opened the trading GUI)",
        #     labels=("player",),
        # ),
        "target_hit": CounterMetricFamily(
            name="mc_player_hit_target",
            documentation="The number of times the player has shot a target block",
            labels=("player",),
        ),
        # "play_one_minute": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The total amount of time played",
        #     labels=("player",),
        # ),
        # "time_since_death": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The time since the player's last death",
        #     labels=("player",),
        # ),
        # "time_since_rest": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The time since the player's last rest. This is used to spawn phantoms",
        #     labels=("player",),
        # ),
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
        # "trigger_trapped_chest": CounterMetricFamily(
        #     name="mc_player_",
        #     documentation="The number of times the player opened trapped chests",
        #     labels=("player",),
        # ),
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
                else:
                    metrics[item].add_metric((name,), value)
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
        # elif item.startswith("clean_"):
        #     metrics["clean"].add_metric((name, item[len("clean_"):]), value)
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
