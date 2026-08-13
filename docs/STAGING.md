# Single staging gate

Status: **pending**. No Chisel runtime, browser, or owner-acceptance result has
been recorded for this implementation.

Reuse the disposable Minecraft/BlueMap server and PVC. Install the exact All
the Mons 1.2.0 Chisel/Athena pair and only the candidate add-on under review in
BlueMap's packs directory. Use a bounded map named `chisel_staging`. The CTM
artifact is not an add-on input or dependency; never supply it to generation,
activation, or verification.

Before startup apply the shared low-cost test settings:

```ini
advance_time=false
advance_weather=false
random_tick_speed=0
spread_vines=false
spawn_mobs=false
spawn_monsters=false
spawn_patrols=false
spawn_phantoms=false
spawn_wandering_traders=false
spawn_wardens=false
spawner_blocks_work=false
pvp=false
player_movement_check=false
freeze_damage=false
fire_damage=false
fall_damage=false
drowning_damage=false
raids=false
global_sound_events=false
```

Run one enabled lifecycle:

1. Install the deterministic gallery datapack, start once, run
   `function chisel_gallery:build`, then `function chisel_gallery:verify`.
   Require exactly 478 logical cases and 744 verified placements with zero
   failures:

   - 439 isolated routed swatches;
   - 31 CTM 3×3 structures, 279 placements;
   - six giant 2×2 structures, 24 placements;
   - two stock controls, two placements.

2. Save and restart once. Rerun only the verifier and require the same
   744/744 result.
3. Require exact Chisel/Athena and resource-schema activation, collision-safe
   coexistence with the Chipped add-on, and no adapter, resource, fallback, or
   render fault. Purge/render only the bounded gallery map.
4. Require nonempty rendered models for every census block. Inspect a bounded
   matrix of all face-local CTM relationships, same-ID seam suppression,
   transparent glass/ice, crimson log-border first-frame output, giant phase
   across positive/negative coordinates, stock weighted variants, caves,
   lighting, UV orientation, and map color.
5. Open the exact external `#chisel_staging` view in the agent browser and
   quickly check for a blank, black, missing, or grossly broken result before
   presenting the link to the owner.
6. Record owner visual acceptance only after the owner explicitly accepts the
   exact candidate JAR and view.

After acceptance, record the candidate JAR size/digests, CI identity, gallery
result, restart result, render audit, browser sanity check, and acceptance date
in release documentation. Until then, do not add an accepted-result section or
claim the implementation is released.
