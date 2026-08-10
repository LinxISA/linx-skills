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

    def test_compiler_uses_v058_pto_engine_contract(self) -> None:
        text = (ROOT / "linx-compiler" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "isa/v0.58/linxisa-v0.58.json",
            "35 VEC + 52 SFU + 10 TLSU + 12 CUBE",
            "TEPL is only the unchanged",
            "exact ten TLSU functions",
            "v0.58 is the sole active stable ISA release",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "--spec /Users/zhoubot/linx-isa/isa/v0.57/",
            "generated from the live v0.57",
            "exact 120-operation map",
            "98 TEPL + 9 TMA + 13 CUBE",
        ):
            self.assertNotIn(forbidden, text)

    def test_qemu_uses_v058_pto_engine_contract(self) -> None:
        text = (ROOT / "linx-qemu" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "isa/v0.58/linxisa-v0.58.json",
            "35 VEC + 52 SFU + 10 TLSU +",
            "12 CUBE",
            "TEPL remains only the unchanged Mode/Function",
            "exact v0.58 set `0..8,13`",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "--spec /Users/zhoubot/linx-isa/isa/v0.57/",
            "live standalone v0.57 catalog",
            "0.57.1 map of exactly 120 direct operations",
            "98 TEPL + 9 TMA + 13 CUBE",
        ):
            self.assertNotIn(forbidden, text)

    def test_linux_requires_v058_pto_executable_identity(self) -> None:
        text = (ROOT / "linx-linux" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "For PTO ISA 0.58 ELF loading",
            "release `0.58.0`",
            "pto-isa-0.58.0-mode-function-v1",
            "exact v0.58 encoding-projection identity",
        ):
            self.assertIn(required, text)
        self.assertNotIn("For PTO ISA 0.57.1 ELF loading", text)


if __name__ == "__main__":
    unittest.main()
