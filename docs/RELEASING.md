# Release procedure

No release exists yet. Complete every gate below before changing the status
from unreleased or recording a production JAR identity.

## Authoritative clean gate

Pull-request CI is the authoritative clean build. It must reacquire only the
two exact third-party inputs, verify their byte identities, check deterministic
profile generation and the full resource/schema contract, run Python and Java
tests, compile with warnings as errors, enforce production/source JAR
boundaries, and generate Maven metadata in one pass:

```bash
gradle --no-daemon \
  -PchiselJar=/absolute/path/chisel-neoforge-2.0.1+mc1.21.1.jar \
  -PathenaJar=/absolute/path/athena-neoforge-1.21.1-4.0.6.jar \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

The CTM artifact must not be supplied to or consulted by this gate. Inspect
the exact production JAR and expanded metadata. Reject NeoForge metadata,
nested JARs, third-party classes, `chisel:*` assets, tests, gallery files,
research evidence, or unexpanded placeholders.

## Runtime and owner gate

Run the single staging lifecycle in [STAGING.md](STAGING.md) against the exact
clean-build JAR. Require the 478-case/744-placement census, one clean restart,
bounded BlueMap render, targeted diagnostics, and no route or render faults.
Open the exact intended BlueMap link in the agent browser for the required
lightweight visual sanity check, then obtain owner visual acceptance.

Do not preserve or publish a runtime, browser, or owner result that was not
actually observed. Do not substitute a locally rebuilt JAR after staging.

## Publication

Before tagging:

1. Confirm the reviewed commit, clean repository, version, changelog,
   provenance, exact generated profile, and CI result.
2. Confirm the staged JAR is byte-identical to the intended release asset and
   record its size and cryptographic digests.
3. Merge version changes through a pull request.
4. Create annotated tag `v<addon_version>` on the reviewed main commit.

The tag workflow may then rebuild from the exact two inputs, publish immutable
GitHub prerelease assets and matching GitHub Packages coordinates, and deploy
nothing. Never move a published tag or replace a release asset.
