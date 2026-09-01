# Changelog

## 0.1.0-alpha.3 - 2026-09-01

- Migrate the adapter boundary to the exact BlueMap 5.23 feature backport.
- Compile the four exact Adapter API `0.1.0-alpha.2` sources from their pinned
  gitlink and bundle their MIT license, but not the standalone module JAR.
- Preserve the accepted Chisel renderer, profile, gallery, and Athena source
  module behavior in the reviewed 254,642-byte production JAR, SHA-256
  `6043a34368dd6fd4d345762121dc99df4cdb23626e367f3f3b1e9b59c12261ef`.

## 0.1.0-alpha.2 - 2026-08-30

- Source-bundle the released `bluemap-athena-resource-models`
  `0.1.0-alpha.1` module at commit
  `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`.
- Remove the four local duplicate model sources while retaining the exhaustive
  256-mask, face-basis, giant-phase, emitter, gallery, and exact-input tests.
- Fail closed when the module gitlink, index, checkout HEAD, source tree, or
  worktree differs from the reviewed pin. Keep every Chisel-specific profile,
  emitter, texture, route, collision, and fallback boundary local.

## 0.1.0-alpha.1 - 2026-08-13

- Add the initial exact Chisel `2.0.1+mc1.21.1` plus Athena `4.0.6` profile
  for All the Mons 1.2.0.
- Route exactly 439 blockstates: 306 Athena CTM models and 133 Athena giant
  models. Keep 854 blockstates stock, including all 117 weighted variants.
- Pin a 3,379-path resource closure containing 439 blockstates, 439 models,
  and 2,501 PNGs, with 2,195 routed role-texture keys.
- Add deterministic first-frame handling for the five known animated crimson
  log-border texture keys; animation playback remains excluded.
- Adapt the owner-authored MIT BlueMap Chipped renderer foundation into
  collision-safe Chisel-specific IDs, exact activation, atomic stock fallback,
  and a plain BlueMap packaging boundary.
- Add a deterministic staging gallery with 478 logical cases and 744 verified
  placements.
- Pass the authoritative pull-request CI gate at commit
  `97801303993ebd6e9ad718c94c6bc6a9a7376060` (tree
  `2e422c0efda8b7e8484f6bce84cc20460cbcae55`) and accept its exact 249,972-byte
  production JAR, SHA-256
  `053e048f9332094571b25b2edc5ddb9a172e1f89c0a65c2f7ceb05e4a946510e`.
- Pass the initial and persisted-restart gallery verifiers with exact scores
  439/37/2/744/0 for swatches/structures/controls/checked/failures.
- Pass the 442,043-byte canonical raw-render audit, SHA-256
  `422ed5738e7807a893247c9ea395b168e2e22bb6fd5261056d8c20978f0677d4`,
  and the lightweight agent-browser sanity check.
- Record owner visual acceptance of the exact candidate on 2026-08-13.

This section records the accepted and published `0.1.0-alpha.1` baseline.
