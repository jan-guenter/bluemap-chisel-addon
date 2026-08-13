# Visual coverage

The closed profile routes exactly 439 of the exact Chisel JAR's 1,293
blockstates:

| Athena loader | Routed blocks |
| --- | ---: |
| CTM | 306 |
| giant | 133 |
| **Total** | **439** |

The other 854 blockstates remain on BlueMap's stock renderer. That stock set
contains exactly 117 weighted-variant blockstates; none is flattened or
claimed by the synthetic route.

## Resource closure

| Resource class | Exact paths |
| --- | ---: |
| Blockstates | 439 |
| Models | 439 |
| PNG textures | 2,501 |
| **Total** | **3,379** |

The routed definitions contain 2,195 Athena role-texture keys. This closure is
a schema and identity contract, not bundled content: all JSON and PNG bytes
come from the operator-installed Chisel/Athena resource roots.

The owned set includes eight glass blocks and ten ice blocks. CTM accounts for
all eight glass and six ice blocks; giant accounts for the other four ice
blocks. Culling and occlusion stay alpha-sensitive.

## Included optics

- Face-local CTM connectivity from all 256 eight-neighbor masks on every cube
  face, with four independently selected quadrants.
- Same-state connection checks and same-native-ID internal-face suppression;
  different IDs and appearance proxies do not connect.
- Stable giant roles `1` through `4` across all faces and positive/negative
  absolute coordinates, including east, north, and down mirroring.
- Installed texture pixels, transparent glass/ice behavior, surface/cave
  geometry, bounded face lighting, UV/winding, and normalized map color.
- Deterministic first-frame output for exactly these animated keys:

  - `chisel:block/ctm/log_bordered/crimson_planks/0`
  - `chisel:block/ctm/log_bordered/crimson_planks/2`
  - `chisel:block/ctm/log_bordered/crimson_planks/3`
  - `chisel:block/ctm/log_bordered/crimson_planks/4`
  - `chisel:block/log_bordered/crimson_planks`

The first four keys are active CTM roles; the fifth is the base-model texture.
Animation playback, interpolation, and time-dependent frames are excluded.

## Accepted deterministic gallery

The staging contract contains 478 logical cases and 744 placements:

| Case group | Logical cases | Placements |
| --- | ---: | ---: |
| Routed isolated swatches | 439 | 439 |
| CTM 3×3 structures | 31 | 279 |
| Giant 2×2 structures | 6 | 24 |
| Stock controls | 2 | 2 |
| **Total** | **478** | **744** |

The exact gallery completed its initial build/verify and its verifier again
after a clean same-pod restart. Both passes reported 439 swatches, 37
structures, two controls, 744 checked placements, and zero failures. The
canonical raw-render audit was 442,043 bytes with SHA-256
`422ed5738e7807a893247c9ea395b168e2e22bb6fd5261056d8c20978f0677d4`;
it passed its bounded geometry, CTM, giant, transparency, deterministic
first-frame, material, and stock-control checks.

The unit/static test contract includes all 256 CTM masks on all faces, giant
phase behavior on both sides of zero, transparency, cave/surface emission,
lighting, atomic fallback, registry collisions, and the 117 weighted stock
controls. The runtime render passed the lightweight agent-browser sanity check
and received owner visual acceptance on 2026-08-13.

Transient presentation state, animation playback, block entities, NBT,
displayed contents, live cross-mod appearance proxies, and generalized
Athena/CTM/Fusion compatibility are excluded. Malformed inputs use atomic
stock fallback.
