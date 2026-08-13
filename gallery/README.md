# Chisel staging gallery

This deterministic datapack defines the accepted exact-profile runtime census:

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

Status: the initial build/verify and persisted verifier after one clean
same-pod restart both completed with exact scores of 439 swatches, 37
structures, two controls, 744 checked placements, and zero failures. The
canonical 442,043-byte raw-render audit (SHA-256
`422ed5738e7807a893247c9ea395b168e2e22bb6fd5261056d8c20978f0677d4`)
passed, the exact external view passed the lightweight agent-browser sanity
check, and the owner accepted the visuals on 2026-08-13. These results apply
only to the 249,972-byte CI JAR with SHA-256
`053e048f9332094571b25b2edc5ddb9a172e1f89c0a65c2f7ceb05e4a946510e`
at commit `97801303993ebd6e9ad718c94c6bc6a9a7376060`.
