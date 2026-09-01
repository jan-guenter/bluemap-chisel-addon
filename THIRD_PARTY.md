# Third-party and source-provenance components

## Adapted implementation source

| Component | Use | Exact identity | License | Binary/assets bundled |
| --- | --- | --- | --- | --- |
| BlueMap Chipped Add-on | Implementation-code origin outside the extracted pure model classes; MIT source adapted and specialized for Chisel | `https://github.com/jan-guenter/bluemap-chipped-addon`, tag `v0.1.0-alpha.1`, commit `c474a82b6bfd1b4173d119cb1e053a5458167e4b` | MIT | No |
| BlueMap Athena Resource Models | First-party pure connection and face model source | `0.1.0-alpha.1`, commit `4a503a63f7f10b7c414c6c1228207a5ba00bfd54`, source tree `882689c2f9a0875547f4e30aefd68659103d5046` | MIT | Four sources compile into this add-on; no module JAR |
| BlueMap Add-on Adapter API | First-party BlueMap 5.23 adapter boundary source | `0.1.0-alpha.2`, commit `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree `2f974c9bb2ba13888d69682f86f30f58922d30eb` | MIT | Four sources compile into this add-on; separate license included; no module JAR |

## Runtime, evidence, and build components

| Component | Use | Exact identity | Declared license/evidence status | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile/runtime host ABI | `5.22-feature.backport-5.23-stateless-java-web-server-46`, implementation commit `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac`, API commit `285c9a60eff3ac2b0cab308ce1058d1565be0971` | MIT | No |
| Chisel | Operator-installed resource owner | `2.0.1+mc1.21.1`, 8,268,524 bytes, SHA-256 `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6` | Exact NeoForge descriptor declares `GPLv2`; source reference `b399d0f` is reference-only because its source archive contains no license file | No |
| Athena | Installed renderer-format identity and resources | `4.0.6`, 99,944 bytes, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5` | MIT | No |
| JetBrains annotations | Compile-only dependency | `23.0.0` | Apache-2.0 | No |
| JUnit | Tests | `5.11.4` | EPL-2.0 | No |
| Checkstyle | Source style | `10.18.2` | LGPL-2.1-or-later | No |
| Gradle | CI build tool | `9.6.1` | Apache-2.0 | No |

The Chisel source reference is not an implementation input, a license
attestation, or a reproducible-build claim. No Chisel or Athena code is copied
or adapted. The packaged profile contains only factual identifiers, loader
families, resource keys/paths, byte sizes, schemas, counts, and hashes; it
contains no third-party resource bytes.

The CTM mod artifact was consulted only as research evidence. It is never a
build input, runtime dependency, activation input, publication input, or
packaged component.
