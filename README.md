# BlueMap Chisel Add-on

An exact-profile BlueMap 5.22 add-on for the Athena-backed connected models in
the Chisel build shipped by All the Mons 1.2.0.

## Status and compatibility

Version `0.1.0-alpha.1` is an **owner-accepted release candidate**. Pull-request
CI, the isolated runtime lifecycle, the canonical raw-render audit, the agent
browser sanity check, and owner visual acceptance all succeeded on 2026-08-13.
Publication and immutable release identity are still pending.

The accepted candidate is commit
`97801303993ebd6e9ad718c94c6bc6a9a7376060` (tree
`2e422c0efda8b7e8484f6bce84cc20460cbcae55`). Its authoritative CI production
JAR is 249,972 bytes with SHA-256
`053e048f9332094571b25b2edc5ddb9a172e1f89c0a65c2f7ceb05e4a946510e`.

The only supported input tuple is:

- Chisel `2.0.1+mc1.21.1`, file
  `chisel-neoforge-2.0.1+mc1.21.1.jar`, 8,268,524 bytes, SHA-256
  `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6`;
- Athena `4.0.6`, file `athena-neoforge-1.21.1-4.0.6.jar`, 99,944 bytes,
  SHA-256
  `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5`;
- Minecraft `1.21.1`, NeoForge `21.1.248`, Java `21`;
- BlueMap backport `5.22-agent.backport-5.22-mc1.21.1-2` at commit
  `9be321df995a1103808621d529eb72773e719d4d`.

The route begins inactive. It activates only when both installed JARs match
their pinned byte identities and the active owned resources retain the exact
blockstate, model, and texture-key schemas. Pixel-only resource-pack overrides
remain usable. An artifact, schema, resource, or registry mismatch keeps the
whole route on BlueMap's original renderer.

The CTM mod artifact is not part of this contract. It was research evidence
only and is never an input, dependency, or packaged component.

## Visual scope

The exact Chisel JAR has 1,293 blockstates. This add-on routes only the 439
whose exact models use one of two Athena loaders:

| Loader | Routed blocks |
| --- | ---: |
| CTM | 306 |
| Giant 2×2 | 133 |

The other 854 blockstates remain stock, including exactly 117 weighted-variant
blockstates. The pinned resource closure is 3,379 paths: 439 blockstates, 439
models, and 2,501 PNGs. The routed definitions reference 2,195 Athena role
texture keys.

CTM faces sample eight same-state, face-local neighbors and select four
quadrant textures from `particle`, `vertical`, `horizontal`, `center`, and
`empty` roles. Only an adjacent block with the same native block ID suppresses
the shared face. Giant faces select roles `1` through `4` from stable absolute
coordinates with face-oriented mirroring. Eight glass and ten ice blocks are
included; transparency remains alpha-sensitive.

Five crimson log-border texture keys carry animation metadata in the exact
resources. This add-on deliberately renders their first frame only, giving
deterministic map output; animation playback is excluded.

Malformed state or a per-block render failure discards partial geometry and
map color before delegating to the original renderer. Live appearance/camo
proxies, NBT, block entities, and frequently changing presentation state are
out of scope.

The deterministic staging gallery completed 478 logical cases and 744 verified
placements: 439 routed swatches, 31 CTM 3×3 structures, six giant 2×2
structures, and two stock controls. Both the initial build/verify and the
persisted same-pod restart verifier reported exact scores of 439 swatches, 37
structures, two controls, 744 checked placements, and zero failures.

The canonical raw-render audit was 442,043 bytes with SHA-256
`422ed5738e7807a893247c9ea395b168e2e22bb6fd5261056d8c20978f0677d4`.
It passed the bounded geometry, CTM, giant-role, transparent glass/ice,
first-frame animation, material, and stock-control checks. The exact external
`#chisel_staging` view passed the required lightweight agent-browser sanity
check before the owner accepted its visuals on 2026-08-13.

See [coverage](docs/COVERAGE.md), [architecture](docs/ARCHITECTURE.md),
[compatibility](docs/COMPATIBILITY.md), [provenance](docs/PROVENANCE.md), and
the [staging gate](docs/STAGING.md).

## Authoritative review gate

Use Java 21 and the exact sibling BlueMap checkout. Supply the two exact
operator-downloaded inputs once:

```bash
gradle --no-daemon \
  -PchiselJar=/absolute/path/chisel-neoforge-2.0.1+mc1.21.1.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

CI reacquires both inputs ephemerally, verifies their exact bytes and the full
profile/resource contract, and discards them. The build bundles no Chisel or
Athena code or assets.

After review and publication, tagged releases will provide production/source
JARs, POM, module metadata, and checksums on GitHub Releases and Maven
coordinates `io.github.jan-guenter:bluemap-chisel-addon:<version>` on GitHub
Packages. A release tag must equal `v<addon_version>`.

## Installation

Once a build has been reviewed and released, place only its plain add-on JAR
in BlueMap's `config/bluemap/packs` directory and restart the JVM. It is not a
NeoForge mod and does not belong in the server's `mods` directory. Removal plus
one restart restores stock rendering; the add-on writes no world or player
data.

## License and provenance

This project is released under the [MIT License](LICENSE). Its implementation
adapts the owner's MIT
[BlueMap Chipped Add-on](https://github.com/jan-guenter/bluemap-chipped-addon)
at tag `v0.1.0-alpha.1`, commit
`c474a82b6bfd1b4173d119cb1e053a5458167e4b`. No Chisel or Athena source or
assets are copied. See [THIRD_PARTY.md](THIRD_PARTY.md),
[NOTICE.md](NOTICE.md), and [docs/PROVENANCE.md](docs/PROVENANCE.md).
