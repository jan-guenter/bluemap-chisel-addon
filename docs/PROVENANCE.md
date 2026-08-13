# Provenance

The machine-readable artifact lock is
`src/main/resources/bluemap-chisel/profiles/exact-artifacts.json`. The exact
generated profile is under
`src/main/resources/bluemap-chisel/profiles/chisel/2.0.1-athena-4.0.6/`, and
the source/evidence declaration is [provenance/upstreams.json](../provenance/upstreams.json).

## Exact runtime evidence

The All the Mons 1.2.0 artifact evidence establishes these required inputs:

- Chisel `chisel-neoforge-2.0.1+mc1.21.1.jar`: 8,268,524 bytes, SHA-1
  `def703bf88cb3bb2960260418e8b36fe47a53dfd`, SHA-256
  `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6`,
  SHA-512
  `ae24678e328e33c989d1dfafa235dc6f0a05ddecaed5acf55842ec20478fab7086f4fb2f634c327bcc402857f44057cea33ded879e582d95e3ebe465748817df`;
- Athena `athena-neoforge-1.21.1-4.0.6.jar`: 99,944 bytes, SHA-1
  `4bcbdf388bd5e387beca7c627224aac33584b55b`, SHA-256
  `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5`,
  SHA-512
  `ab40a306a26ce834daae921a1e87768cd2538a4bfe27a4480f97af854084cc334e7416b1bd0b7583834a32a86951283f29fd4b1df7b98a967a6b26a3ec05e2cf`.

The generator verifies filenames, sizes, hashes, the complete 1,293 Chisel
blockstate roster, the 306 CTM and 133 giant route rosters, all 439 model IDs,
2,195 role-texture IDs, 117 excluded weighted variants, every active loader
and model schema, and the 3,379-path resource closure. Generated output
contains identifiers, schemas, counts, sizes, and hashes—not upstream resource
bytes.

## Implementation source

The sole implementation-code provenance is the owner-authored MIT
[BlueMap Chipped Add-on](https://github.com/jan-guenter/bluemap-chipped-addon)
at tag `v0.1.0-alpha.1`, commit
`c474a82b6bfd1b4173d119cb1e053a5458167e4b`. Its exact-profile activation,
BlueMap adapter/emitter, CTM and giant selection, reversible fallback, tests,
and build/release foundation were adapted into a collision-safe Chisel
namespace and specialized for this closed resource profile.

No Chisel or Athena implementation source is copied or adapted. The Chisel
artifact's exact NeoForge descriptor declares `GPLv2`. Source reference
`b399d0f` is retained only as a reference because its source archive contains
no license file; it is not a license attestation, source-to-binary attestation,
reproducible-build claim, or implementation input. Athena's exact artifact
declares MIT, but its source is likewise not used by this implementation.

## Resource and excluded evidence lanes

At build/profile time, Chisel and Athena are black-box artifacts used to
derive and verify factual resource schemas, identifiers, hashes, and counts.
At runtime, the add-on consumes only operator-installed JSON/PNG resources
after the exact pair and active schema have passed validation. No third-party
model, texture, translation, capture, mesh, source, class, or binary is
committed or packaged.

The CTM mod artifact was evidence-only during research. It is intentionally
absent from the generator input contract, compile/runtime dependencies,
activation logic, publication inputs, and packaged output.

This provenance record describes an unreleased implementation. It makes no
runtime, owner-acceptance, publication, or release-artifact identity claim.
