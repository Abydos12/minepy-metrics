from typing import Dict

from prometheus_client.metrics_core import CounterMetricFamily

from src.utils import get_player_stats


def generate_player_stats_metrics() -> Dict[str, CounterMetricFamily]:
    return {
        "use_item": CounterMetricFamily(
            name="mc_player_use_item",
            documentation="number of item utilization",
            labels=["player", "mod", "item"],
        ),
        "craft_item": CounterMetricFamily(
            name="mc_player_craft_item",
            documentation="number",
            labels=["player", "mod", "item"],
        ),
        "mine_block": CounterMetricFamily(
            name="mc_player_mine_block",
            documentation="number",
            labels=["player", "mod", "item"],
        ),
        "pickup": CounterMetricFamily(
            name="mc_player_pickup",
            documentation="number",
            labels=["player", "mod", "item"],
        ),
        "kill_entity": CounterMetricFamily(
            name="mc_player_kill_entity",
            documentation="number",
            labels=["player", "entity"],
        ),
        "drop": CounterMetricFamily(
            name="mc_player_drop",
            documentation="number",
            labels=["player", "mod", "item"],
        ),
        "furnace_interaction": CounterMetricFamily(
            name="mc_player_furnace_interaction",
            documentation="number",
            labels=["player"],
        ),
        "deaths": CounterMetricFamily(
            name="mc_player_deaths", documentation="number", labels=["player"]
        ),
        "fish_caught": CounterMetricFamily(
            name="mc_player_fish_caught", documentation="number", labels=["player"]
        ),
        "chest_opened": CounterMetricFamily(
            name="mc_player_chest_opened", documentation="number", labels=["player"]
        ),
        "crouch_one_cm": CounterMetricFamily(
            name="mc_player_crouch_one_cm", documentation="number", labels=["player"]
        ),
        "crafting_table_interaction": CounterMetricFamily(
            name="mc_player_crafting_table_interaction",
            documentation="number",
            labels=["player"],
        ),
        "sprint_one_cm": CounterMetricFamily(
            name="mc_player_sprint_one_cm", documentation="number", labels=["player"]
        ),
        "brewingstand_interaction": CounterMetricFamily(
            name="mc_player_brewingstand_interaction",
            documentation="number",
            labels=["player", "entity"],
        ),
        "entity_killed_by": CounterMetricFamily(
            name="mc_player_entity_killed_by",
            documentation="number",
            labels=["player", "killer"],
        ),
        "mob_kills": CounterMetricFamily(
            name="mc_player_mob_kills", documentation="number", labels=["player"]
        ),
        "hopper_inspected": CounterMetricFamily(
            name="mc_player_hopper_inspected", documentation="number", labels=["player"]
        ),
        "trapped_chest_triggered": CounterMetricFamily(
            name="mc_player_trapped_chest_triggered",
            documentation="number",
            labels=["player"],
        ),
        "horse_one_cm": CounterMetricFamily(
            name="mc_player_horse_one_cm", documentation="number", labels=["player"]
        ),
        "climb_one_cm": CounterMetricFamily(
            name="mc_player_climb_one_cm", documentation="number", labels=["player"]
        ),
        "damage_dealt": CounterMetricFamily(
            name="mc_player_damage_dealt", documentation="number", labels=["player"]
        ),
        "leave_game": CounterMetricFamily(
            name="mc_player_leave_game", documentation="number", labels=["player"]
        ),
        "item_enchanted": CounterMetricFamily(
            name="mc_player_item_enchanted", documentation="number", labels=["player"]
        ),
        "cake_slices_eaten": CounterMetricFamily(
            name="mc_player_cake_slices_eaten",
            documentation="number",
            labels=["player"],
        ),
        "fly_one_cm": CounterMetricFamily(
            name="mc_player_fly_one_cm", documentation="number", labels=["player"]
        ),
        "time_since_death": CounterMetricFamily(
            name="mc_player_time_since_death", documentation="number", labels=["player"]
        ),
        "dive_one_cm": CounterMetricFamily(
            name="mc_player_dive_one_cm", documentation="number", labels=["player"]
        ),
        "jump": CounterMetricFamily(
            name="mc_player_jump", documentation="number", labels=["player"]
        ),
        "damage_taken": CounterMetricFamily(
            name="mc_player_damage_taken", documentation="number", labels=["player"]
        ),
        "animals_bred": CounterMetricFamily(
            name="mc_player_animals_bred", documentation="number", labels=["player"]
        ),
        "play_one_minute": CounterMetricFamily(
            name="mc_player_play_one_minute", documentation="number", labels=["player"]
        ),
        "fall_one_cm": CounterMetricFamily(
            name="mc_player_fall_one_cm", documentation="number", labels=["player"]
        ),
        "sneak_time": CounterMetricFamily(
            name="mc_player_sneak_time", documentation="number", labels=["player"]
        ),
        "swim_one_cm": CounterMetricFamily(
            name="mc_player_swim_one_cm", documentation="number", labels=["player"]
        ),
        "dispenser_inspected": CounterMetricFamily(
            name="mc_player_dispenser_inspected",
            documentation="number",
            labels=["player"],
        ),
        "sleep_in_bed": CounterMetricFamily(
            name="mc_player_sleep_in_bed", documentation="number", labels=["player"]
        ),
        "walk_one_cm": CounterMetricFamily(
            name="mc_player_walk_one_cm", documentation="number", labels=["player"]
        ),
    }


def setup_player_stats_metrics(uuid: str, name: str) -> Dict:
    metrics = generate_player_stats_metrics()
    for key, value in get_player_stats(uuid).items():
        key = key.split(".")[1:]  # ignore "stat"
        if "useItem" == key[0]:
            metrics["use_item"].add_metric(labels=[name, key[1], key[2]], value=value)
        elif "craftItem" == key[0]:
            metrics["craft_item"].add_metric(labels=[name, key[1], key[2]], value=value)
        elif "mineBlock" == key[0]:
            metrics["mine_block"].add_metric(labels=[name, key[1], key[2]], value=value)
        elif "pickup" == key[0]:
            metrics["pickup"].add_metric(labels=[name, key[1], key[2]], value=value)
        elif "killEntity" == key[0]:
            metrics["kill_entity"].add_metric(
                labels=[name, ".".join(key[1:])], value=value
            )
        elif "drop" == key[0] and len(key) > 1:  # exclude "stat.drop"
            metrics["drop"].add_metric(labels=[name, key[1], key[2]], value=value)
        elif "furnaceInteraction" == key[0]:
            metrics["furnace_interaction"].add_metric(labels=[name], value=value)
        elif "deaths" == key[0]:
            metrics["deaths"].add_metric(labels=[name], value=value)
        elif "fishCaught" == key[0]:
            metrics["fish_caught"].add_metric(labels=[name], value=value)
        elif "chestOpened" == key[0]:
            metrics["chest_opened"].add_metric(labels=[name], value=value)
        elif "crouchOneCm" == key[0]:
            metrics["crouch_one_cm"].add_metric(labels=[name], value=value)
        elif "craftingTableInteraction" == key[0]:
            metrics["crafting_table_interaction"].add_metric(labels=[name], value=value)
        elif "sprintOneCm" == key[0]:
            metrics["sprint_one_cm"].add_metric(labels=[name], value=value)
        elif "brewingstandInteraction" == key[0]:
            metrics["brewingstand_interaction"].add_metric(labels=[name], value=value)
        elif "entityKilledBy" == key[0]:
            metrics["entity_killed_by"].add_metric(
                labels=[name, ".".join(key[1:])], value=value
            )
        elif "mobKills" == key[0]:
            metrics["mob_kills"].add_metric(labels=[name], value=value)
        elif "hopperInspected" == key[0]:
            metrics["hopper_inspected"].add_metric(labels=[name], value=value)
        elif "trappedChestTriggered" == key[0]:
            metrics["trapped_chest_triggered"].add_metric(labels=[name], value=value)
        elif "horseOneCm" == key[0]:
            metrics["horse_one_cm"].add_metric(labels=[name], value=value)
        elif "climbOneCm" == key[0]:
            metrics["climb_one_cm"].add_metric(labels=[name], value=value)
        elif "damageDealt" == key[0]:
            metrics["damage_dealt"].add_metric(labels=[name], value=value)
        elif "leaveGame" == key[0]:
            metrics["leave_game"].add_metric(labels=[name], value=value)
        elif "itemEnchanted" == key[0]:
            metrics["item_enchanted"].add_metric(labels=[name], value=value)
        elif "cakeSlicesEaten" == key[0]:
            metrics["cake_slices_eaten"].add_metric(labels=[name], value=value)
        elif "flyOneCm" == key[0]:
            metrics["fly_one_cm"].add_metric(labels=[name], value=value)
        elif "timeSinceDeath" == key[0]:
            metrics["time_since_death"].add_metric(labels=[name], value=value)
        elif "diveOneCm" == key[0]:
            metrics["dive_one_cm"].add_metric(labels=[name], value=value)
        elif "jump" == key[0]:
            metrics["jump"].add_metric(labels=[name], value=value)
        elif "damageTaken" == key[0]:
            metrics["damage_taken"].add_metric(labels=[name], value=value)
        elif "animalsBred" == key[0]:
            metrics["animals_bred"].add_metric(labels=[name], value=value)
        elif (
            "playOneMinute" == key[0]
        ):  # divide by 20 for seconds => https://bugs.mojang.com/browse/MC-29522
            metrics["play_one_minute"].add_metric(labels=[name], value=value)
        elif "fallOneCm" == key[0]:
            metrics["fall_one_cm"].add_metric(labels=[name], value=value)
        elif "sneakTime" == key[0]:
            metrics["sneak_time"].add_metric(labels=[name], value=value)
        elif "swimOneCm" == key[0]:
            metrics["swim_one_cm"].add_metric(labels=[name], value=value)
        elif "dispenserInspected" == key[0]:
            metrics["dispenser_inspected"].add_metric(labels=[name], value=value)
        elif "sleepInBed" == key[0]:
            metrics["sleep_in_bed"].add_metric(labels=[name], value=value)
        elif "walkOneCm" == key[0]:
            metrics["walk_one_cm"].add_metric(labels=[name], value=value)
    return metrics
