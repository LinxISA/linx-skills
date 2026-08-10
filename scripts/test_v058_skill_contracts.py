from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V058SkillContractsTest(unittest.TestCase):
    def test_linx_isa_uses_current_engine_and_hard_break_contract(self) -> None:
        text = (ROOT / "linx-isa" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "four semantic execution engines are exactly",
            "`VEC`, `TLSU`, `CUBE`, and",
            "`TEPL` remains the unchanged encoded carrier",
            "active `TFMA`",
            "`B.IOD` and `BSTART.PAR` are permanently deleted",
            "--profile v0.58",
            "check_canonical_v058.py",
            "check_pto_v058_manifest.py",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "--profile v0.57",
            "check_canonical_v057.py",
            "check_pto_v057_manifest.py",
            "TFMA` are deleted",
        ):
            self.assertNotIn(forbidden, text)

    def test_superproject_routes_current_components_only(self) -> None:
        text = (ROOT / "linx-superproject" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "component-lock.v0.58.json",
            "tools/Linx-TileOP-API",
            "workloads/pto_kernels/benchmarks/supernpu",
            "workloads/SuperNPUBench` is forbidden",
            "check_component_lock.py",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "--profile v0.57",
            "check_canonical_v057.py",
            "check_pto_v057_manifest.py",
            "--case avs-pto-parity",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
