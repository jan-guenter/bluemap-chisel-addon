#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the metadata-only exact Chisel/Athena rendering profile."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
import zipfile


PROFILE_ROOT = Path("src/main/resources/bluemap-chisel/profiles")
PROFILE_DIRECTORY = PROFILE_ROOT / "chisel/2.0.1-athena-4.0.6"
CATALOG_PATH = PROFILE_ROOT / "exact-artifacts.json"
PROFILE_PATH = PROFILE_DIRECTORY / "profile.json"
DEFINITIONS_PATH = PROFILE_DIRECTORY / "definitions.tsv"
RESOURCES_PATH = PROFILE_DIRECTORY / "required-resources.tsv"

CHISEL_FILENAME = "chisel-neoforge-2.0.1+mc1.21.1.jar"
CHISEL_SIZE = 8_268_524
CHISEL_SHA1 = "def703bf88cb3bb2960260418e8b36fe47a53dfd"
CHISEL_SHA256 = "66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6"
CHISEL_SHA512 = (
    "ae24678e328e33c989d1dfafa235dc6f0a05ddecaed5acf55842ec20478fab708"
    "6f4fb2f634c327bcc402857f44057cea33ded879e582d95e3ebe465748817df"
)
ATHENA_FILENAME = "athena-neoforge-1.21.1-4.0.6.jar"
ATHENA_SIZE = 99_944
ATHENA_SHA1 = "4bcbdf388bd5e387beca7c627224aac33584b55b"
ATHENA_SHA256 = "43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5"
ATHENA_SHA512 = (
    "ab40a306a26ce834daae921a1e87768cd2538a4bfe27a4480f97af854084cc334"
    "e7416b1bd0b7583834a32a86951283f29fd4b1df7b98a967a6b26a3ec05e2cf"
)

ALL_BLOCKSTATES_COUNT = 1_293
ALL_BLOCKSTATES_DIGEST = (
    "4f03295eb5c1dd7b85615791de1db9d8a43f9578894dfa142443af94ac9e8926"
)
ROSTER_COUNT = 439
ROSTER_DIGEST = "a8bd7f297fe1a6423fe68327b99bf3e08112f2f93bc94c52c12873c2d027f7e4"
MODEL_COUNT = 439
MODEL_DIGEST = "a103f0db28500724e45d4144f63753b1a39ee4c0c3b1b2d429e04040a0dd765b"
ROLE_TEXTURE_COUNT = 2_195
ROLE_TEXTURE_DIGEST = "41818f1aecfbfa2fabd5733b27c41fc6374261b0b5881ea965084d8f5f9720ca"
PNG_COUNT = 2_501
RESOURCE_PATH_COUNT = 3_379
STOCK_WEIGHTED_COUNT = 117
STOCK_WEIGHTED_DIGEST = (
    "bb1c4209fa99e1f45152d9d83fe6ae0105943f0b364f32275efb8659694617e9"
)

LOADERS: dict[str, tuple[int, str, tuple[str, ...], str]] = {
    "athena:ctm": (
        306,
        "630d1645d31499060862d070b1857ad0b5e7f5cd1bebefd6559eee9db4eaa45e",
        ("particle", "empty", "center", "vertical", "horizontal"),
        "block/cube_all",
    ),
    "athena:giant": (
        133,
        "75c76c2a474a4ca009cb88c8d4fc87c1f8e0b95e7548f02161da2725bd1c96a4",
        ("particle", "1", "2", "3", "4"),
        "block/cube_all",
    ),
}

ANIMATED_TEXTURES = {
    "chisel:block/ctm/log_bordered/crimson_planks/0",
    "chisel:block/ctm/log_bordered/crimson_planks/2",
    "chisel:block/ctm/log_bordered/crimson_planks/3",
    "chisel:block/ctm/log_bordered/crimson_planks/4",
    "chisel:block/log_bordered/crimson_planks",
}


def digest_bytes(raw: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, raw).hexdigest()


def digest_path(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def roster_digest(values: Iterable[str]) -> str:
    payload = "".join(f"{value}\n" for value in sorted(values)).encode("utf-8")
    return digest_bytes(payload)


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def resource_path(key: str, kind: str, suffix: str) -> str:
    if ":" in key:
        namespace, value = key.split(":", 1)
    else:
        namespace, value = "minecraft", key
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe resource key: {key}")
    return f"assets/{namespace}/{kind}/{value}{suffix}"


def verify_file_identity(
    path: Path, *, filename: str, size: int, sha1: str, sha256: str, sha512: str
) -> None:
    if not path.is_file() or path.name != filename:
        raise ValueError(f"unexpected artifact path: {path}")
    if path.stat().st_size != size:
        raise ValueError(f"unexpected artifact size for {path}")
    for algorithm, expected in (
        ("sha1", sha1),
        ("sha256", sha256),
        ("sha512", sha512),
    ):
        actual = digest_path(path, algorithm)
        if actual != expected:
            raise ValueError(
                f"{path.name} {algorithm} changed: got {actual}, expected {expected}"
            )


def _model_texture_map(model: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    textures = model.get("textures")
    if not isinstance(textures, dict) or not textures:
        raise ValueError("ordinary model has no texture map")
    rows: list[str] = []
    for key, value in sorted(textures.items()):
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("ordinary model texture map is malformed")
        rows.append(f"{key}={value}\n")
    return digest_bytes("".join(rows).encode("utf-8")), tuple(
        value for _key, value in sorted(textures.items())
    )


def _parse_definition(
    archive: zipfile.ZipFile, path: str, raw: bytes
) -> tuple[tuple[str, ...], str, tuple[str, ...], tuple[str, ...]] | None:
    value = json.loads(raw)
    if not isinstance(value, dict) or "athena:loader" not in value:
        return None
    loader = value.get("athena:loader")
    if loader not in LOADERS:
        raise ValueError(f"{path} has unsupported Athena loader {loader!r}")
    expected_count, _digest, roles, parent = LOADERS[loader]
    del expected_count

    expected_keys = {"athena:loader", "ctm_textures", "variants"}
    if loader == "athena:giant":
        expected_keys.update(("width", "height"))
        if value.get("width") != 2 or value.get("height") != 2:
            raise ValueError(f"{path} giant dimensions changed")
    if set(value) != expected_keys:
        raise ValueError(f"{path} blockstate schema changed")

    variants = value.get("variants")
    if not isinstance(variants, dict) or set(variants) != {""}:
        raise ValueError(f"{path} variants changed")
    variant = variants[""]
    if not isinstance(variant, dict) or set(variant) != {"model"}:
        raise ValueError(f"{path} default variant changed")
    model_key = variant.get("model")
    if not isinstance(model_key, str):
        raise ValueError(f"{path} model key is malformed")

    textures = value.get("ctm_textures")
    if not isinstance(textures, dict) or set(textures) != set(roles):
        raise ValueError(f"{path} Athena texture schema changed")
    texture_values = tuple(textures[role] for role in roles)
    if any(not isinstance(texture, str) for texture in texture_values):
        raise ValueError(f"{path} Athena texture key is malformed")

    model_path = resource_path(model_key, "models", ".json")
    try:
        model = json.loads(archive.read(model_path))
    except KeyError as error:
        raise ValueError(f"missing ordinary model {model_path}") from error
    if not isinstance(model, dict) or set(model) != {"parent", "textures"}:
        raise ValueError(f"{model_path} ordinary model schema changed")
    if model.get("parent") != parent:
        raise ValueError(f"{model_path} parent changed")

    block = path.removeprefix("assets/chisel/blockstates/").removesuffix(".json")
    model_texture_digest, model_textures = _model_texture_map(model)
    row = (
        f"chisel:{block}",
        loader.removeprefix("athena:"),
        model_key,
        parent,
        *texture_values,
        model_texture_digest,
    )
    return row, model_path, texture_values, model_textures


def build_outputs(chisel: Path, athena: Path) -> dict[Path, bytes]:
    verify_file_identity(
        chisel,
        filename=CHISEL_FILENAME,
        size=CHISEL_SIZE,
        sha1=CHISEL_SHA1,
        sha256=CHISEL_SHA256,
        sha512=CHISEL_SHA512,
    )
    verify_file_identity(
        athena,
        filename=ATHENA_FILENAME,
        size=ATHENA_SIZE,
        sha1=ATHENA_SHA1,
        sha256=ATHENA_SHA256,
        sha512=ATHENA_SHA512,
    )

    definitions: list[tuple[str, ...]] = []
    family_blocks: dict[str, list[str]] = {loader: [] for loader in LOADERS}
    all_blocks: list[str] = []
    model_keys: set[str] = set()
    texture_keys: set[str] = set()
    required_paths: set[str] = set()
    stock_weighted: list[str] = []

    with zipfile.ZipFile(chisel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Chisel JAR contains duplicate ZIP entries")
        for path in sorted(names):
            prefix = "assets/chisel/blockstates/"
            if not path.startswith(prefix) or not path.endswith(".json"):
                continue
            bare_block = path[len(prefix) : -len(".json")]
            all_blocks.append(bare_block)
            raw_blockstate = archive.read(path)
            parsed = _parse_definition(archive, path, raw_blockstate)
            if parsed is None:
                value = json.loads(raw_blockstate)
                variants = value.get("variants", {}) if isinstance(value, dict) else {}
                if isinstance(variants, dict) and any(
                    isinstance(variant, list)
                    or isinstance(variant, dict) and variant.get("weight", 1) != 1
                    for variant in variants.values()
                ):
                    stock_weighted.append(bare_block)
                continue
            row, model_path, textures, model_textures = parsed
            definitions.append(row)
            loader = f"athena:{row[1]}"
            family_blocks[loader].append(bare_block)
            model_keys.add(row[2])
            texture_keys.update(textures)
            required_paths.add(path)
            required_paths.add(model_path)
            required_paths.update(
                resource_path(texture, "textures", ".png") for texture in textures
            )
            required_paths.update(
                resource_path(texture, "textures", ".png")
                for texture in model_textures
            )

        if len(all_blocks) != ALL_BLOCKSTATES_COUNT:
            raise ValueError("Chisel blockstate count changed")
        if roster_digest(all_blocks) != ALL_BLOCKSTATES_DIGEST:
            raise ValueError("Chisel complete blockstate roster changed")
        for loader, (count, expected_digest, _roles, _parent) in LOADERS.items():
            values = family_blocks[loader]
            if len(values) != count or roster_digest(values) != expected_digest:
                raise ValueError(f"{loader} roster changed")
        routed = [block for values in family_blocks.values() for block in values]
        if len(routed) != ROSTER_COUNT or roster_digest(routed) != ROSTER_DIGEST:
            raise ValueError("Chisel Athena-loader roster changed")
        if (len(stock_weighted) != STOCK_WEIGHTED_COUNT
                or roster_digest(stock_weighted) != STOCK_WEIGHTED_DIGEST):
            raise ValueError("Chisel weighted stock roster changed")
        if len(model_keys) != MODEL_COUNT or roster_digest(model_keys) != MODEL_DIGEST:
            raise ValueError("Chisel Athena model roster changed")
        if (len(texture_keys) != ROLE_TEXTURE_COUNT
                or roster_digest(texture_keys) != ROLE_TEXTURE_DIGEST):
            raise ValueError("Chisel Athena texture roster changed")

        animated = {
            path.removeprefix("assets/").replace("/textures/", ":", 1)
            .removesuffix(".png.mcmeta")
            for path in names
            if path.startswith("assets/chisel/textures/")
            and path.endswith(".png.mcmeta")
        }
        if animated != ANIMATED_TEXTURES:
            raise ValueError("Chisel animated texture roster changed")
        for texture in sorted(ANIMATED_TEXTURES):
            metadata_path = resource_path(texture, "textures", ".png.mcmeta")
            metadata = json.loads(archive.read(metadata_path))
            if metadata != {"animation": {"interpolate": True, "frametime": 10}}:
                raise ValueError(f"{metadata_path} animation schema changed")

        resource_rows: list[str] = []
        resource_bytes = 0
        for path in sorted(required_paths):
            try:
                raw = archive.read(path)
            except KeyError as error:
                raise ValueError(f"missing required Chisel resource {path}") from error
            resource_rows.append(f"{path}\t{len(raw)}\t{digest_bytes(raw)}\n")
            resource_bytes += len(raw)
        if (len(resource_rows) != RESOURCE_PATH_COUNT
                or sum(path.endswith(".png") for path in required_paths) != PNG_COUNT):
            raise ValueError("Chisel exact resource closure changed")

    definitions.sort(key=lambda row: row[0])
    definitions_raw = "".join("\t".join(row) + "\n" for row in definitions).encode(
        "ascii"
    )
    resources_raw = "".join(resource_rows).encode("ascii")
    definitions_digest = digest_bytes(definitions_raw)
    resources_digest = digest_bytes(resources_raw)

    family_counts = {
        loader.removeprefix("athena:"): LOADERS[loader][0]
        for loader in sorted(LOADERS)
    }
    family_digests = {
        loader.removeprefix("athena:"): LOADERS[loader][1]
        for loader in sorted(LOADERS)
    }
    catalog = {
        "schemaVersion": 1,
        "baseline": {
            "packVersion": "1.2.0",
            "packRepositoryCommit": "c7bb230f21d14d26859d0b92548f089b3a493ad9",
            "minecraft": "1.21.1",
            "neoforge": "21.1.248",
            "java": 21,
        },
        "requiredForStaticRendering": ["chisel", "athena"],
        "artifacts": [
            {
                "modId": "chisel",
                "metadataVersion": "2.0.1+mc1.21.1",
                "filename": CHISEL_FILENAME,
                "sizeBytes": CHISEL_SIZE,
                "sha1": CHISEL_SHA1,
                "sha256": CHISEL_SHA256,
                "sha512": CHISEL_SHA512,
                "licenseDeclaration": "GPLv2 in exact NeoForge descriptor",
                "sourceUseLane": "black-box/resource-interpreter",
                "curseForgeProjectId": 551763,
                "curseForgeFileId": 8288925,
                "modrinthProjectId": "4KWv7wbN",
                "modrinthVersionId": "4ItA9dOc",
                "verificationRole": "consumer-resource-owner",
            },
            {
                "modId": "athena",
                "metadataVersion": "4.0.6",
                "filename": ATHENA_FILENAME,
                "sizeBytes": ATHENA_SIZE,
                "sha1": ATHENA_SHA1,
                "sha256": ATHENA_SHA256,
                "sha512": ATHENA_SHA512,
                "license": "MIT",
                "curseForgeProjectId": 841890,
                "curseForgeFileId": 8061947,
                "curseForgeFingerprint": 669268138,
                "modrinthProjectId": "b1ZV3DIJ",
                "modrinthVersionId": "dJgL278E",
                "verificationRole": "renderer-format-identity",
            },
        ],
    }
    profile = {
        "schemaVersion": 1,
        "profileId": "chisel-athena-2.0.1-4.0.6",
        "minecraft": "1.21.1",
        "neoforge": "21.1.248",
        "chiselVersion": "2.0.1+mc1.21.1",
        "athenaVersion": "4.0.6",
        "coverage": {
            "allChiselBlockstates": ALL_BLOCKSTATES_COUNT,
            "allChiselBlockstatesDigest": ALL_BLOCKSTATES_DIGEST,
            "routedBlocks": ROSTER_COUNT,
            "routedBlocksDigest": ROSTER_DIGEST,
            "stockBlocks": ALL_BLOCKSTATES_COUNT - ROSTER_COUNT,
            "stockWeightedVariants": STOCK_WEIGHTED_COUNT,
            "stockWeightedVariantsDigest": STOCK_WEIGHTED_DIGEST,
            "loaderCounts": family_counts,
            "loaderDigests": family_digests,
            "modelCount": MODEL_COUNT,
            "modelDigest": MODEL_DIGEST,
            "roleTextureCount": ROLE_TEXTURE_COUNT,
            "roleTextureDigest": ROLE_TEXTURE_DIGEST,
            "pngCount": PNG_COUNT,
            "resourcePathCount": RESOURCE_PATH_COUNT,
            "animatedTextureCount": len(ANIMATED_TEXTURES),
        },
        "definitionCatalog": {
            "path": "definitions.tsv",
            "rows": len(definitions),
            "sha256": definitions_digest,
        },
        "resourceClosure": {
            "path": "required-resources.tsv",
            "rows": len(resource_rows),
            "bytes": resource_bytes,
            "sha256": resources_digest,
        },
        "runtimePolicy": {
            "resourceSource": "operator-installed roots only",
            "pixelOverrides": "allowed when all schema and texture IDs remain exact",
            "schemaOverrides": "deactivate the route and preserve stock rendering",
            "nonNativeAppearanceProxies": "stock fallback",
            "animation": "deterministic first frame; playback excluded",
        },
    }
    outputs = {
        CATALOG_PATH: json.dumps(catalog, indent=2, sort_keys=True).encode("utf-8")
        + b"\n",
        PROFILE_PATH: json.dumps(profile, indent=2, sort_keys=True).encode("utf-8")
        + b"\n",
        DEFINITIONS_PATH: definitions_raw,
        RESOURCES_PATH: resources_raw,
    }
    return outputs


def apply_outputs(outputs: dict[Path, bytes], *, check: bool) -> None:
    mismatches: list[str] = []
    for path, expected in outputs.items():
        if check:
            if not path.is_file() or path.read_bytes() != expected:
                mismatches.append(str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
    if mismatches:
        raise ValueError("generated profile is stale: " + ", ".join(mismatches))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chisel", required=True, type=Path)
    parser.add_argument("--athena", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs(args.chisel, args.athena)
    apply_outputs(outputs, check=args.check)
    action = "verified" if args.check else "generated"
    print(f"{action} exact Chisel/Athena profile ({ROSTER_COUNT} routed blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
