# Removal and rollback

The add-on writes no world, player, or required configuration state. For a
reviewed installation, remove only its JAR from BlueMap's packs directory,
restart the BlueMap JVM, and rerender affected regions to restore stock output.

An artifact, active-schema, resource, or registry mismatch keeps the complete
439-block route inactive. An individual observation/render failure discards
partial output and delegates that whole block to BlueMap's original renderer.
No legacy, relaxed, or partial-version fallback profile is maintained.

Use an immutable published release as the rollback artifact. Do not use an
unpublished candidate build for operational rollback.
