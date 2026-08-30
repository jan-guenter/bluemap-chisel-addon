# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha2_candidate_seals_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(1, release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.2", release["version"])
        self.assertEqual("v0.1.0-alpha.2", release["tag"])
        self.assertEqual(
            {
                "production_jar": {
                    "file_name": "bluemap-chisel-addon-0.1.0-alpha.2.jar",
                    "size": 251_223,
                    "sha256": "0b4fcb7221d7d0bd103397ed6e61e87cf694f1dffdbf61cd811f7ea592675610",
                },
                "sources_jar": {
                    "file_name": "bluemap-chisel-addon-0.1.0-alpha.2-sources.jar",
                    "size": 216_727,
                    "sha256": "2d6c926a1d539a41447cddd4afc1084a51056b3ae5175b285d2e046bf7013302",
                },
                "pom": {
                    "file_name": "bluemap-chisel-addon-0.1.0-alpha.2.pom",
                    "size": 1_335,
                    "sha256": "5ba3219033d244a54dd7e359c90526d4237d99199d3b9ce7b2ddfb798df5103c",
                },
                "gradle_module": {
                    "file_name": "bluemap-chisel-addon-0.1.0-alpha.2.module.json",
                    "size": 2_813,
                    "sha256": "a5fa28e1334114f6fd30d92f7d54ef8adf4f843117d2090432a8d0aead872cbe",
                },
            },
            release["final_release_artifacts"],
        )

    def test_alpha2_candidate_records_the_bounded_athena_migration(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(
            {
                "module_repository": "https://github.com/jan-guenter/bluemap-athena-resource-models",
                "module_version": "0.1.0-alpha.1",
                "module_tag": "v0.1.0-alpha.1",
                "module_commit": "4a503a63f7f10b7c414c6c1228207a5ba00bfd54",
                "module_source_tree": "882689c2f9a0875547f4e30aefd68659103d5046",
                "removed_local_model_sources": 4,
                "renderer_or_gallery_behavior_change": False,
            },
            release["athena_model_migration"],
        )
        self.assertEqual(
            {
                "production_jar_exact_byte_gate": True,
                "sources_jar_exact_byte_gate": True,
                "publication_metadata_exact_byte_gate": True,
                "exact_input_gate": True,
                "reproducibility_gate": True,
                "hostile_gitlink_trust_probes": True,
            },
            release["verification"],
        )


if __name__ == "__main__":
    unittest.main()
