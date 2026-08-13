#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the bounded exhaustive Chisel/Athena staging gallery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
DEFINITIONS = (
    REPOSITORY
    / "src/main/resources/bluemap-chisel/profiles/chisel/"
    / "2.0.1-athena-4.0.6/definitions.tsv"
)
SWATCH_ORIGIN = (-72, 100, -82)
SWATCH_COLUMNS = 23
STRUCTURAL_ORIGIN = (-72, 100, -34)
STRUCTURAL_COLUMNS = 8


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int
    z: int

    def offset(self, dx: int = 0, dy: int = 0, dz: int = 0) -> "Position":
        return Position(self.x + dx, self.y + dy, self.z + dz)

    def command(self) -> str:
        return f"{self.x} {self.y} {self.z}"


@dataclass(frozen=True)
class Placement:
    position: Position
    block: str
    routed: bool = True


@dataclass(frozen=True)
class Fixture:
    case_id: str
    family: str
    anchor: Position
    placements: tuple[Placement, ...]
    notes: str


def definitions() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in DEFINITIONS.read_text(encoding="ascii").splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            raise ValueError("malformed definitions catalog")
        rows.append((fields[0], fields[1]))
    if len(rows) != 439 or len({block for block, _family in rows}) != 439:
        raise ValueError("exact routed definition census changed")
    families = {family: sum(item[1] == family for item in rows)
                for family in {item[1] for item in rows}}
    if families != {"ctm": 306, "giant": 133}:
        raise ValueError(f"exact routed family census changed: {families}")
    return rows


def swatches(rows: Iterable[tuple[str, str]]) -> list[Placement]:
    x0, y, z0 = SWATCH_ORIGIN
    result: list[Placement] = []
    for index, (block, _family) in enumerate(rows):
        result.append(Placement(Position(
            x0 + 2 * (index % SWATCH_COLUMNS),
            y,
            z0 + 2 * (index // SWATCH_COLUMNS),
        ), block))
    return result


def structural_fixtures() -> list[Fixture]:
    result: list[Fixture] = []

    def anchor(index: int) -> Position:
        x0, y, z0 = STRUCTURAL_ORIGIN
        return Position(
            x0 + 9 * (index % STRUCTURAL_COLUMNS),
            y,
            z0 + 9 * (index // STRUCTURAL_COLUMNS),
        )

    ctm_blocks = (
        "chisel:bubble/glass",
        "chisel:chrono/glass",
        "chisel:light/glass",
        "chisel:noborder/glass",
        "chisel:ornatesteel/glass",
        "chisel:shale/glass",
        "chisel:steelframe/glass",
        "chisel:stone/glass",
        "chisel:circular/ice",
        "chisel:dent/ice",
        "chisel:encased_bricks/ice",
        "chisel:large_tile/ice",
        "chisel:mosaic/ice",
        "chisel:weaver/ice",
        "chisel:log_bordered/crimson_planks",
        "chisel:array/diorite",
        "chisel:array/granite",
        "chisel:braid/acacia_planks",
        "chisel:braid/birch_planks",
        "chisel:braid/crimson_planks",
        "chisel:braid/dark_oak_planks",
        "chisel:braid/jungle_planks",
        "chisel:braid/oak_planks",
        "chisel:braid/spruce_planks",
        "chisel:circular/andesite",
        "chisel:circular/black_concrete",
        "chisel:circular/blue_concrete",
        "chisel:circular/bricks",
        "chisel:circular/brown_concrete",
        "chisel:circular/coal_block",
        "chisel:circular/cobblestone",
    )
    for index, block in enumerate(ctm_blocks):
        center = anchor(index)
        placements = tuple(
            Placement(center.offset(dx, 0, dz), block)
            for dz in (-1, 0, 1)
            for dx in (-1, 0, 1)
        )
        result.append(Fixture(
            f"ctm-3x3-{index:02d}",
            "ctm",
            center,
            placements,
            "3x3 all-neighbor, seam, culling, and transparency witness",
        ))

    # Each giant fixture exposes a complete 2x2 phase on three face planes.
    giant_cases = (
        ("array-andesite-xz", "chisel:array/andesite", "xz"),
        ("array-ice-xz", "chisel:array/ice", "xz"),
        ("jellybean-cobblestone-xy", "chisel:jellybean/cobblestone", "xy"),
        ("jellybean-ice-xy", "chisel:jellybean/ice", "xy"),
        ("slant-quartz-yz", "chisel:slant/quartz", "yz"),
        ("zag-ice-yz", "chisel:zag/ice", "yz"),
    )
    plane_offsets = {
        "xz": ((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1)),
        "xy": ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)),
        "yz": ((0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)),
    }
    for offset, (case_id, block, plane) in enumerate(giant_cases, start=31):
        center = anchor(offset)
        placements = tuple(
            Placement(center.offset(dx, dy, dz), block)
            for dx, dy, dz in plane_offsets[plane]
        )
        result.append(Fixture(
            f"giant-2x2-{case_id}",
            "giant",
            center,
            placements,
            f"2x2 {plane.upper()} coordinate-phase and mirroring witness",
        ))

    if len(result) != 37:
        raise AssertionError(f"gallery has {len(result)} structural cases")
    occupied: set[Position] = set()
    for fixture in result:
        for placement in fixture.placements:
            if placement.position in occupied:
                raise AssertionError(f"fixture overlap at {placement.position}")
            occupied.add(placement.position)
    return result


def controls() -> list[Placement]:
    return [
        Placement(Position(9, 100, 2), "chisel:braid/coal_block", False),
        Placement(Position(12, 100, 2), "minecraft:stone", False),
    ]


def swatches_tsv(rows: list[tuple[str, str]], blocks: list[Placement]) -> str:
    lines = ["index\tblock_id\tloader_family\tx\ty\tz"]
    for index, ((block_id, family), placement) in enumerate(
            zip(rows, blocks, strict=True)):
        lines.append(
            f"{index}\t{block_id}\t{family}\t{placement.position.x}\t"
            f"{placement.position.y}\t{placement.position.z}"
        )
    return "\n".join(lines) + "\n"


def cases_tsv(fixtures: list[Fixture], stock: list[Placement]) -> str:
    lines = ["case_id\tfamily\tx\ty\tz\tplacements\tnotes"]
    for fixture in fixtures:
        lines.append(
            f"{fixture.case_id}\t{fixture.family}\t{fixture.anchor.x}\t"
            f"{fixture.anchor.y}\t{fixture.anchor.z}\t"
            f"{len(fixture.placements)}\t{fixture.notes}"
        )
    for index, item in enumerate(stock):
        lines.append(
            f"stock-{index}\tstock\t{item.position.x}\t{item.position.y}\t"
            f"{item.position.z}\t1\tstock renderer control: {item.block}"
        )
    return "\n".join(lines) + "\n"


def clear_function() -> str:
    lines = ["# Generated by gallery/generate.py; do not edit."]
    for x0 in range(-80, 21, 20):
        lines.append(f"fill {x0} 99 -88 {x0 + 19} 104 12 minecraft:air")
    return "\n".join(lines) + "\n"


def build_function(
        swatch_blocks: list[Placement], fixtures: list[Fixture],
        stock: list[Placement]) -> str:
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "function chisel_gallery:clear",
        "fill -80 99 -88 39 99 12 minecraft:stone",
        "scoreboard players set #swatches chisel_gallery 0",
        "scoreboard players set #structures chisel_gallery 0",
        "scoreboard players set #controls chisel_gallery 0",
    ]
    for placement in swatch_blocks:
        lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #swatches chisel_gallery 1")
    for fixture in fixtures:
        for placement in fixture.placements:
            lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #structures chisel_gallery 1")
    for placement in stock:
        lines.append(f"setblock {placement.position.command()} {placement.block}")
        lines.append("scoreboard players add #controls chisel_gallery 1")
    lines.extend((
        "function chisel_gallery:verify",
        "tellraw @a [{\"text\":\"Chisel gallery: \"},{\"score\":{\"name\":\"#checked\",\"objective\":\"chisel_gallery\"}},{\"text\":\" checked placements, \"},{\"score\":{\"name\":\"#failures\",\"objective\":\"chisel_gallery\"}},{\"text\":\" failures\"}]",
    ))
    return "\n".join(lines) + "\n"


def verify_function(
        swatch_blocks: list[Placement], fixtures: list[Fixture],
        stock: list[Placement]) -> str:
    placements = [*swatch_blocks]
    placements.extend(item for fixture in fixtures for item in fixture.placements)
    placements.extend(stock)
    if len(placements) != 744:
        raise AssertionError(f"gallery has {len(placements)} placements")
    lines = [
        "# Generated by gallery/generate.py; do not edit.",
        "scoreboard players set #failures chisel_gallery 0",
        "scoreboard players set #checked chisel_gallery 0",
    ]
    for placement in placements:
        lines.append(
            f"execute unless block {placement.position.command()} {placement.block} run "
            "scoreboard players add #failures chisel_gallery 1"
        )
        lines.append("scoreboard players add #checked chisel_gallery 1")
    lines.extend((
        "execute unless score #checked chisel_gallery matches 744 run scoreboard players add #failures chisel_gallery 1",
        "execute unless score #swatches chisel_gallery matches 439 run scoreboard players add #failures chisel_gallery 1",
        "execute unless score #structures chisel_gallery matches 37 run scoreboard players add #failures chisel_gallery 1",
        "execute unless score #controls chisel_gallery matches 2 run scoreboard players add #failures chisel_gallery 1",
    ))
    return "\n".join(lines) + "\n"


def rendered_files() -> dict[Path, bytes]:
    rows = definitions()
    swatch_blocks = swatches(rows)
    fixtures = structural_fixtures()
    stock = controls()
    placement_count = (
        len(swatch_blocks)
        + sum(len(case.placements) for case in fixtures)
        + len(stock)
    )
    logical_cases = len(swatch_blocks) + len(fixtures) + len(stock)
    if placement_count != 744 or logical_cases != 478:
        raise AssertionError("gallery census changed")
    files: dict[Path, bytes] = {
        Path("swatches.tsv"): swatches_tsv(rows, swatch_blocks).encode("utf-8"),
        Path("cases.tsv"): cases_tsv(fixtures, stock).encode("utf-8"),
        Path("cases.json"): (json.dumps({
            "schema_version": 1,
            "baseline": {
                "pack": "All the Mons 1.2.0",
                "minecraft": "1.21.1",
                "chisel": "2.0.1+mc1.21.1",
                "athena": "4.0.6",
            },
            "routed_swatch_count": len(swatch_blocks),
            "structural_case_count": len(fixtures),
            "stock_control_count": len(stock),
            "logical_case_count": logical_cases,
            "verified_placement_count": placement_count,
            "structural_cases": [
                {
                    "case_id": case.case_id,
                    "family": case.family,
                    "anchor": {
                        "x": case.anchor.x,
                        "y": case.anchor.y,
                        "z": case.anchor.z,
                    },
                    "notes": case.notes,
                    "placements": [
                        {
                            "x": item.position.x,
                            "y": item.position.y,
                            "z": item.position.z,
                            "block": item.block,
                            "expected_route": "custom",
                        }
                        for item in case.placements
                    ],
                }
                for case in fixtures
            ],
            "stock_controls": [
                {
                    "x": item.position.x,
                    "y": item.position.y,
                    "z": item.position.z,
                    "block": item.block,
                    "expected_route": "stock-control",
                }
                for item in stock
            ],
        }, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        Path("datapack/pack.mcmeta"): (json.dumps({
            "pack": {
                "description": "ATM 1.2.0 Chisel/Athena BlueMap review gallery",
                "pack_format": 48,
            }
        }, indent=2) + "\n").encode("utf-8"),
        Path("datapack/data/minecraft/tags/function/load.json"): (
            json.dumps({"values": ["chisel_gallery:load"]}, indent=2) + "\n"
        ).encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/load.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "scoreboard objectives add chisel_gallery dummy\n"
            "forceload add -80 -96 48 16\n"
        ).encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/build.mcfunction"):
            build_function(swatch_blocks, fixtures, stock).encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/verify.mcfunction"):
            verify_function(swatch_blocks, fixtures, stock).encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/clear.mcfunction"):
            clear_function().encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/pose.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "tp @s -18.5 145 35.5 180 38\n"
        ).encode("utf-8"),
        Path("datapack/data/chisel_gallery/function/release.mcfunction"): (
            "# Generated by gallery/generate.py; do not edit.\n"
            "forceload remove -80 -96 48 16\n"
        ).encode("utf-8"),
    }
    checksums = [
        f"{hashlib.sha256(content).hexdigest()}  {path.as_posix()}"
        for path, content in sorted(files.items(), key=lambda item: item[0].as_posix())
    ]
    files[Path("SHA256SUMS")] = ("\n".join(checksums) + "\n").encode("ascii")
    return files


def write_or_check(files: dict[Path, bytes], check: bool) -> int:
    differences: list[str] = []
    for relative, expected in files.items():
        path = ROOT / relative
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                differences.append(relative.as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if differences:
        print("generated gallery differs: " + ", ".join(differences), file=sys.stderr)
        return 1
    if not check:
        print("generated 478-case / 744-placement Chisel gallery")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return write_or_check(rendered_files(), args.check)


if __name__ == "__main__":
    raise SystemExit(main())
