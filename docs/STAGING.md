# Single staging gate

Status: **accepted on 2026-08-13** for the exact candidate below. Publication
and immutable release identity remain separate gates.

## Accepted result

- Candidate commit:
  `97801303993ebd6e9ad718c94c6bc6a9a7376060`; tree
  `2e422c0efda8b7e8484f6bce84cc20460cbcae55`.
- Authoritative pull-request CI production JAR: 249,972 bytes; SHA-256
  `053e048f9332094571b25b2edc5ddb9a172e1f89c0a65c2f7ceb05e4a946510e`.
- Initial build/verify scores: 439 swatches, 37 structures, two controls, 744
  checked placements, zero failures.
- Persisted verifier scores after one clean same-pod restart: 439 swatches, 37
  structures, two controls, 744 checked placements, zero failures.
- Canonical raw-render audit: 442,043 bytes; SHA-256
  `422ed5738e7807a893247c9ea395b168e2e22bb6fd5261056d8c20978f0677d4`.
  The bounded geometry, CTM, giant-role/phase, transparent glass/ice,
  deterministic animation-frame, material, and stock-control checks passed.
- The exact external `#chisel_staging` view loaded without an obvious blank,
  black, missing, or grossly broken result in the agent browser before it was
  presented for inspection.
- The owner explicitly accepted that candidate and view on 2026-08-13.

The following procedure remains the reproducible lifecycle for this accepted
result.

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

The accepted result above is evidence for this exact candidate only. A rebuilt
or changed JAR requires a new byte-identity check; a changed supported input
tuple requires a fresh staging and owner-review cycle.
