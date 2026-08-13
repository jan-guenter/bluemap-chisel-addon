#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail-closed review gate for exact Chisel 2.0.1/Athena 4.0.6."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile

import generate_profile


def _verify_mod_metadata(chisel: Path, athena: Path) -> None:
    with zipfile.ZipFile(chisel) as archive:
        try:
            metadata = archive.read("META-INF/neoforge.mods.toml")
        except KeyError as error:
            raise ValueError("missing Chisel NeoForge metadata") from error
        if b'"chisel"' not in metadata or b'"2.0.1+mc1.21.1"' not in metadata:
            raise ValueError("Chisel NeoForge metadata identity changed")
        names = archive.namelist()
        if not any(name.startswith("assets/chisel/") for name in names):
            raise ValueError("Chisel archive has no installed resource root")
        if any(name.startswith("earth/terrarium/athena/") for name in names):
            raise ValueError("Chisel archive unexpectedly embeds Athena classes")

    with zipfile.ZipFile(athena) as archive:
        names = archive.namelist()
        if "META-INF/neoforge.mods.toml" not in names:
            raise ValueError("Athena archive has no NeoForge metadata")
        metadata = archive.read("META-INF/neoforge.mods.toml")
        if b'"athena"' not in metadata or b'"4.0.6"' not in metadata:
            raise ValueError("Athena NeoForge metadata identity changed")
        if not any(name.startswith("earth/terrarium/athena/") for name in names):
            raise ValueError("Athena archive has no expected implementation package")


def verify(chisel: Path, athena: Path) -> None:
    outputs = generate_profile.build_outputs(chisel, athena)
    generate_profile.apply_outputs(outputs, check=True)
    _verify_mod_metadata(chisel, athena)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chisel", required=True, type=Path)
    parser.add_argument("--athena", required=True, type=Path)
    args = parser.parse_args()
    try:
        verify(args.chisel, args.athena)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"artifact verification failed: {error}", file=sys.stderr)
        return 1
    print(
        "Verified exact Chisel 2.0.1+mc1.21.1 + Athena 4.0.6 artifacts, "
        "439 routed definitions, and the metadata-only resource closure."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
