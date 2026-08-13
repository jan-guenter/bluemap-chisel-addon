# Architecture

This repository produces one plain BlueMap add-on JAR. It is not a NeoForge
mod and has no client renderer, world state, packet, bundled dependency, or
required configuration.

```text
BlueMap add-on entrypoint
        |
collision-safe BlueMap 5.22 adapter IDs
        |
exact Chisel + Athena artifact gate
        |
active blockstate/model/texture schema gate
        |
439 immutable definitions (306 CTM + 133 giant)
        |
bounded renderer -> reversible emission -> stock fallback
```

## Activation and resource boundary

The route starts inactive. It requires the exact Chisel
`2.0.1+mc1.21.1` and Athena `4.0.6` byte identities, the exact 439-definition
roster, and matching active blockstate/model/texture-key schemas. The pinned
resource closure has 3,379 paths: 439 blockstates, 439 models, and 2,501 PNGs.
The definitions reference 2,195 role-texture keys.

Higher-priority resource packs may replace PNG pixels while retaining exact
schemas and texture IDs. A changed artifact, roster, loader, model parent,
texture-key set, required resource, or registry ID deactivates the complete
route and preserves BlueMap's stock path. The remaining 854 Chisel
blockstates—including all 117 weighted variants—are never redirected.

The extension installs only operator-provided textures before atlas filtering.
It bundles no `chisel:*` assets. Four animated CTM role textures and one
base-model texture for crimson log-border planks are converted to a
deterministic first frame; playback is intentionally absent.

The CTM mod artifact does not participate in generation, compilation,
activation, rendering, or packaging.

## CTM renderer

For each visible cube face, the CTM renderer samples exactly eight neighbors
in that face's local plane. A connection requires the same native block ID and
the same persisted block state. The unsigned eight-bit mask selects four
quadrant roles from `particle`, `vertical`, `horizontal`, `center`, and
`empty`. Face-local orientation controls both quadrant placement and UVs.

The direct face is suppressed only when the adjacent block has the same native
block ID. Different IDs and non-native appearance proxies do not connect or
hide a face, even if their visual resources resemble one another.

## Giant renderer

Giant models expose roles `1` through `4`. Each face chooses a 2×2 tile from
face-oriented absolute block coordinates. The mapping preserves east, north,
and down mirroring and remains stable across positive and negative world
coordinates. Adjacency does not alter the phase.

## Emission, light, color, and culling

The emitter uses installed texture keys only. It preserves face winding and
UV orientation, emits top faces for the surface pass and other visible faces
for cave geometry, and uses the maximum self/neighbor sky and block light for
each face. Map color is normalized from emitted top-face samples and retains
the maximum sampled top alpha.

Full-cube culling and occlusion are enabled only when the original
`cube_all` model culls and every active renderer-role texture is fully opaque.
For giant models the unused `particle` role is excluded from that decision.
`cullingIdentical` stays false so connected faces are evaluated explicitly.

Each render starts at a recorded tile-model segment and map-color value. A
malformed state, missing texture, invalid observation, or ordinary emission
failure truncates the partial segment, restores map color, and invokes the
original BlueMap renderer for the entire block. Capacity failures propagate
instead of being hidden by fallback.

## Collision isolation

The add-on entrypoint, resource extension, synthetic blockstate/model, and
renderer registration use the `bluemap_chisel` namespace. Registration fails
closed if any expected slot is already occupied. These IDs are deliberately
distinct from the BlueMap Chipped Add-on so both packs can be installed in the
same BlueMap JVM.
