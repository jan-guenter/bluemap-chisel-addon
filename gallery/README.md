# Chisel staging gallery

This deterministic datapack defines the pending exact-profile runtime census:

- 439 isolated, two-block-spaced swatches—one for every routed Chisel ID;
- 31 CTM 3×3 structures (279 placements), spanning opaque, glass, ice, and
  the deterministic crimson log-border first frame;
- six giant 2×2 structures (24 placements) across XZ, XY, and YZ planes;
- two stock-renderer controls: one weighted Chisel block and vanilla stone.

That is exactly 478 logical cases and 744 verified placements. Generate or
check it with `python3 gallery/generate.py --check`, package it with
`gallery/package.sh <output.zip>`, then use:

```text
/function chisel_gallery:build
/function chisel_gallery:verify
/function chisel_gallery:pose
/function chisel_gallery:release
```

The verifier is the bounded server registry/placement census: every generated
placement must retain its exact expected block ID and `#failures
chisel_gallery` must be zero. The datapack contains only IDs, coordinates,
commands, and metadata; it bundles no Chisel or Athena assets.

Status: runtime execution, BlueMap rendering, agent-browser sanity checking,
and owner visual acceptance are pending. Do not treat deterministic generation
as a completed staging result.
