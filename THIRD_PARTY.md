# Third-party and source-provenance components

## Adapted implementation source

| Component | Use | Exact identity | License | Binary/assets bundled |
| --- | --- | --- | --- | --- |
| BlueMap Chipped Add-on | Sole implementation-code provenance; MIT source adapted and specialized for Chisel | `https://github.com/jan-guenter/bluemap-chipped-addon`, tag `v0.1.0-alpha.1`, commit `c474a82b6bfd1b4173d119cb1e053a5458167e4b` | MIT | No |

## Runtime, evidence, and build components

| Component | Use | Exact identity | Declared license/evidence status | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile/runtime host ABI | Backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` | MIT | No |
| Chisel | Operator-installed resource owner | `2.0.1+mc1.21.1`, 8,268,524 bytes, SHA-256 `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6` | Exact NeoForge descriptor declares `GPLv2`; source reference `b399d0f` is reference-only because its source archive contains no license file | No |
| Athena | Installed renderer-format identity and resources | `4.0.6`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` | MIT | No |
| JetBrains annotations | Compile-only dependency | `23.0.0` | Apache-2.0 | No |
| JUnit | Tests | `5.11.4` | EPL-2.0 | No |
| Checkstyle | Source style | `10.18.2` | LGPL-2.1-or-later | No |
| Gradle | CI build tool | `9.4.0` | Apache-2.0 | No |

The Chisel source reference is not an implementation input, a license
attestation, or a reproducible-build claim. No Chisel or Athena code is copied
or adapted. The packaged profile contains only factual identifiers, loader
families, resource keys/paths, byte sizes, schemas, counts, and hashes; it
contains no third-party resource bytes.

The CTM mod artifact was consulted only as research evidence. It is never a
build input, runtime dependency, activation input, publication input, or
packaged component.
