# Compatibility

Compatibility is exact and evidence-locked.

| Component | Required identity |
| --- | --- |
| All the Mons | `1.2.0`, repository commit `c7bb230f21d14d26859d0b92548f089b3a493ad9` |
| Minecraft / NeoForge / Java | `1.21.1` / `21.1.248` / `21` |
| BlueMap | `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` |
| Chisel | `chisel-neoforge-2.0.1+mc1.21.1.jar`, 8,268,524 bytes, SHA-1 `def703bf88cb3bb2960260418e8b36fe47a53dfd`, SHA-256 `66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6`, SHA-512 `ae24678e328e33c989d1dfafa235dc6f0a05ddecaed5acf55842ec20478fab7086f4fb2f634c327bcc402857f44057cea33ded879e582d95e3ebe465748817df` |
| Athena | `athena-neoforge-1.21.1-4.0.6.jar`, 99,944 bytes, SHA-1 `4bcbdf388bd5e387beca7c627224aac33584b55b`, SHA-256 `43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5`, SHA-512 `ab40a306a26ce834daae921a1e87768cd2538a4bfe27a4480f97af854084cc334e7416b1bd0b7583834a32a86951283f29fd4b1df7b98a967a6b26a3ec05e2cf` |

Both runtime artifacts are mandatory. The route additionally validates the
closed 439-block roster and active resource schemas. Pixel-only replacements
are allowed when the blockstate, model, loader, and texture-key contracts stay
exact.

The CTM mod artifact is not required and is never consulted by the add-on. Its
earlier research role does not make it a build dependency, runtime dependency,
activation input, compatibility requirement, or publication input.

This is not a compatibility claim for another Chisel or Athena build, a later
All the Mons release, generalized Athena/CTM/Fusion resources, weighted
variants, or live cross-mod appearance proxies. Chisel source reference
`b399d0f` is reference-only and was not used to implement behavior. Every new
byte tuple needs a new closed profile, clean gate, runtime inspection, browser
sanity check, and owner visual acceptance.

The project remains an unreleased local implementation; the table describes
its intended activation tuple, not a completed runtime certification.
