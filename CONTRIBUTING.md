# Contributing

Open an issue before changing the supported artifact tuple, route roster,
resource closure, loader families, animation policy, or visual scope.
Compatibility is an exact profile, never a version range.

Contributions must be compatible with this project's MIT license. Code may be
adapted from the identified MIT BlueMap Chipped Add-on lineage with attribution.
Do not copy or adapt Chisel or Athena source, classes, models, textures,
translations, captures, or meshes. The CTM mod artifact must remain
evidence-only. All third-party binary/resource inputs stay local and ignored.

Preserve route-wide fail-closed activation and atomic per-block fallback.
Malformed state or a failed render must restore the original geometry and map
color before BlueMap's stock renderer runs; capacity failures must propagate.
New registry IDs must remain collision-safe with the Chipped add-on.

Submit one coherent change and rely on pull-request CI for the authoritative
clean gate in [AGENTS.md](AGENTS.md). Record runtime, browser, and owner-review
claims only after the exact corresponding gate has actually run.
