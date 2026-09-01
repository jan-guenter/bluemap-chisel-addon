# SPDX-License-Identifier: MIT
"""Static release-evidence regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha3_candidate_seals_the_accepted_artifact(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(1, release["schema_version"])
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.3", release["version"])
        self.assertEqual("v0.1.0-alpha.3", release["tag"])
        self.assertEqual(
            {
                "file_name": "bluemap-chisel-addon-0.1.0-alpha.3.jar",
                "size": 254_642,
                "sha256": "6043a34368dd6fd4d345762121dc99df4cdb23626e367f3f3b1e9b59c12261ef",
                "accepted_date": "2026-09-01",
                "local_reproduction_is_byte_exact": True,
            },
            release["accepted_integration_artifact"],
        )

    def test_alpha3_candidate_records_the_source_modules_and_host(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())

        self.assertEqual(
            {
                "repository": "https://github.com/jan-guenter/bluemap-athena-resource-models",
                "version": "0.1.0-alpha.1",
                "tag": "v0.1.0-alpha.1",
                "commit": "4a503a63f7f10b7c414c6c1228207a5ba00bfd54",
                "source_tree": "882689c2f9a0875547f4e30aefd68659103d5046",
            },
            release["athena_model_module"],
        )
        self.assertEqual(
            {
                "repository": "https://github.com/jan-guenter/bluemap-addon-adapter-api",
                "version": "0.1.0-alpha.2",
                "tag": "v0.1.0-alpha.2",
                "commit": "e81f08bc4bfbf02d810ec8949a019130e2e61634",
                "source_tree": "2f974c9bb2ba13888d69682f86f30f58922d30eb",
                "gitlink": "modules/bluemap-addon-adapter-api",
                "standalone_module_jar": "not-bundled-or-installed",
            },
            release["adapter_api_migration"],
        )
        self.assertEqual(
            {
                "bluemap_version": "5.22-feature.backport-5.23-stateless-java-web-server-46",
                "bluemap_commit": "7e07f4e74ec1e92a6ead9aa1e66054af3e133aac",
                "bluemap_api_commit": "285c9a60eff3ac2b0cab308ce1058d1565be0971",
            },
            release["host"],
        )


if __name__ == "__main__":
    unittest.main()
