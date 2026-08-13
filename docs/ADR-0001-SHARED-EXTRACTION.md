# ADR 0001: adapt MIT source without a shared runtime

Status: accepted for the unreleased Chisel implementation.

## Context

The owner-selected implementation strategy is to adapt the existing MIT
[BlueMap Chipped Add-on](https://github.com/jan-guenter/bluemap-chipped-addon)
at tag `v0.1.0-alpha.1`, commit
`c474a82b6bfd1b4173d119cb1e053a5458167e4b`. That project already provides the
exact-profile activation, BlueMap 5.22 adapter, reversible emitter, CTM and
giant selectors, fallback boundaries, packaging, and release mechanics needed
here.

Chisel `2.0.1+mc1.21.1` is a different resource roster and activation tuple.
Its source reference `b399d0f` is reference-only because the source archive
contains no license file. Neither Chisel nor Athena source is an implementation
input.

## Decision

Copy and adapt only the identified MIT Chipped implementation source into a
standalone Chisel repository. Specialize it with:

- collision-safe `bluemap_chisel:*` registry and synthetic-model IDs;
- the exact Chisel/Athena dual-artifact and active-resource gate;
- the closed 439-definition CTM/giant profile;
- deterministic first-frame handling for five known animated texture keys;
- Chisel-specific gallery, tests, provenance, and publication coordinates.

Do not introduce a shared installed runtime or classloader dependency. Do not
copy Chisel or Athena source or assets. The CTM artifact remains evidence-only.

## Why no shared extraction yet

There are now two related repository-local consumers, but no demonstrated
third consumer and no stable neutral API. A shared binary would couple release
and classloader behavior across otherwise removable BlueMap packs. Premature
generalization would also blur each exact resource profile's fail-closed
boundary.

Revisit source extraction only when a concrete third consumer establishes the
same invariants and failure semantics. Any future extraction must retain
standalone packaging, collision-safe registration, exact activation, atomic
fallback, and traceable MIT provenance.
