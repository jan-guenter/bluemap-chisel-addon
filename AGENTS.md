# Agent guide for BlueMap Chisel Add-on

Read `/root/work/allthemons/AGENTS.md` and this file before changing this
repository. This is a standalone public MIT project, not a NeoForge mod and
not part of the root orchestration repository.

## Exact baseline

| Component | Identity |
| --- | --- |
| All the Mons | `1.2.0`, pack commit `c7bb230f21d14d26859d0b92548f089b3a493ad9` |
| Minecraft / NeoForge / Java | `1.21.1` / `21.1.248` / `21` |
| BlueMap | backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` |
| Chisel | `2.0.1+mc1.21.1`, 8,268,524 bytes, SHA-256 `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6` |
| Athena | `4.0.6`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` |

A new pack, BlueMap build, or either changed artifact starts a fresh evidence,
implementation, and visual-review task.

## Project boundaries

- The production artifact is a plain BlueMap add-on JAR. It contains no
  NeoForge metadata, Mixins, nested JARs, client bootstrap, third-party
  classes, or `chisel:*` assets.
- Own exactly 439 Chisel blockstates: 306 exact Athena CTM models and 133 exact
  Athena giant models. Leave the other 854 blockstates on BlueMap's stock
  path, including all 117 stock weighted-variant blockstates.
- Treat the 3,379-path resource closure as exact: 439 blockstates, 439 models,
  and 2,501 PNGs. The two families reference 2,195 role-texture keys.
- Render the five known animated crimson log-border texture keys as a
  deterministic first frame. Animation playback is out of scope.
- Activate only for the exact Chisel/Athena artifact pair and exact active
  resource schemas. Route-wide artifact, schema, closure, registry-collision,
  or resource failures keep every owned block on the stock path.
- Keep per-block fallback atomic: discard partial geometry and map color, then
  call BlueMap's original renderer. Capacity failures must still propagate.
- Use only block identity/properties, eight bounded face-local neighbors, and
  stable absolute coordinates. Live appearance proxies, NBT, block entities,
  and transient presentation state are out of scope.
- The CTM mod artifact is evidence-only. It is never a build input, runtime
  dependency, activation input, or packaged component.
- The implementation adapts the owner's MIT BlueMap Chipped Add-on at tag
  `v0.1.0-alpha.1`, commit
  `c474a82b6bfd1b4173d119cb1e053a5458167e4b`. Do not copy or adapt Chisel or
  Athena source, classes, models, textures, captures, or meshes.

## Validation cadence

Develop in one coherent tranche. Pull-request CI is the authoritative clean
gate; do not repeat it locally after small edits:

```bash
gradle --no-daemon \
  -PchiselJar=/absolute/path/chisel-neoforge-2.0.1+mc1.21.1.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

The implementation remains unreleased until the clean gate, the single
staging lifecycle in [docs/STAGING.md](docs/STAGING.md), the required quick
agent-browser sanity check, and owner visual acceptance all succeed. Never
turn planned or partial evidence into a release or runtime claim.
