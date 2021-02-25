# Minepy-metrics

Strongly inspired by https://github.com/Joshi425/minecraft-exporter

Dockerized prometheus exporter for minecraft. 

## Use

Docker compose example:
```yaml
version: "3.7"
services:
  minepy-metrics:
    image: abydos12/minepy-metrics:latest
    container_name: Minepy-metrics
    environment:
      WORLD_NAME: world
      RCON_HOST: localhost
      RCON_PASSWORD: password
      RCON_PORT: 25575
      FORGE_SERVER: True
    ports:
      - 8000:8000
    volumes:
    - /path/to/serv/folder:/minecraft
```
Write this in a `docker-compose.yml` file then:
```
sudo docker-compose up -d
```

### Environment var

VAR | DEFAULT | description
--- | --- | ---
`WORLD_NAME` | `world` | world's folder name
`RCON_HOST` | `None` | server's ip address
`RCON_PORT` | `25575` | server's rcon port
`RCON_PASSWORD` | `None` | world's folder name
`FORGE_SERVER` | `False` | enable forge metrics (see [Forge metrcis]())

## Metrics

### Global

`mc_players_online`

`mc_player_uuid`

`mc_world_infos` -> `labels`: `version` `difficulty` `game_mode` `hardcore`

### Forge

`mc_player_entities_loaded`

### Player vitals

`mc_player_food_level`

`mc_player_food_saturation_level`

`mc_player_health`

`mc_player_score`

`mc_player_xp_level`

`mc_player_xp_total`

### Player stats

`mc_player_mined`

`mc_player_broken`

`mc_player_crafted`

`mc_player_used`

`mc_player_picked_up`

`mc_player_dropped`

`mc_player_entity_killed`

`mc_player_mob_kills`

`mc_player_killed_by`

`mc_player_animals_bred`

`mc_player_item_cleaned`

`mc_player_interacted`

`mc_player_cauldron_filled`

`mc_player_damage_absorbed`

`mc_player_damage_blocked_by_shield`

`mc_player_damage_dealt`

`mc_player_damage_dealt_absorbed`

`mc_player_damage_dealt_resisted`

`mc_player_damage_resisted`

`mc_player_damage_taken`

`mc_player_distance`

`mc_player_fish_caught`

`mc_player_leave_game`

`mc_player_item_enchanted`

`mc_player_jump`

`mc_player_record_played`

`mc_player_noteblock_played`

`mc_player_noteblock_tuned`

`mc_player_deaths`

`mc_player_plants_potted`

`mc_player_killed_players`

`mc_player_triggered_raid`

`mc_player_won_raid`

`mc_player_hit_target`

`mc_player_time_spend`

`mc_player_slept_in_bed`

`mc_player_traded_with_villager`

`mc_player_used_cauldron`


## Notes
    Support breaking change in player stats file in 1.13 and above
#### players stats
- `stats.drop` not exported, duplicate with `stats.dropped` (sum all items)

#### other
Can't figure out what's the difference between `stats.mob_kills` and `sum(stats.killed)`.
Values are different but why ??? 

Both `stats.mob_kills` and `stats.killed` are exported for now







