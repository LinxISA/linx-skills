from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "linx-cross-model-validation"
SKILL = SKILL_ROOT / "SKILL.md"
PREFLIGHT = SKILL_ROOT / "scripts/preflight_qemu.py"
PROVENANCE = SKILL_ROOT / "scripts/write_provenance.py"


class CrossModelValidationSkillTests(unittest.TestCase):
    def run_preflight(
        self, binary: Path, qemu_root: Path, timeout: float = 2.0
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(PREFLIGHT),
                str(binary),
                "--qemu-root",
                str(qemu_root),
                "--timeout",
                str(timeout),
            ],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )

    def write_executable(self, directory: Path, body: str) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "qemu-system-linx64"
        path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def init_repo(self, path: Path, filename: str) -> str:
        path.mkdir()
        (path / filename).write_text(filename + "\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", str(path)], check=True)
        subprocess.run(["git", "-C", str(path), "add", filename], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(path),
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            check=True,
        )
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
        ).strip()

    def test_preflight_rejects_missing_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            result = self.run_preflight(root / "build-linx/qemu-system-linx64", root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing", result.stderr.lower())

    def test_preflight_rejects_non_executable_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = root / "build-linx/qemu-system-linx64"
            binary.parent.mkdir(parents=True)
            binary.write_text("not executable\n", encoding="utf-8")
            result = self.run_preflight(binary, root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not executable", result.stderr.lower())

    def test_preflight_rejects_wrong_executable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = self.write_executable(root / "build-linx", "print('unrelated tool')\n")
            result = self.run_preflight(binary, root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized probe response", result.stderr.lower())

    def test_preflight_rejects_missing_size_despite_old_sentinel_first_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = self.write_executable(
                root / "build-linx",
                "import json, sys\n"
                "sys.stdin.read()\n"
                "print(json.dumps({'QMP': {'version': {}}}))\n"
                "print(json.dumps({'return': {}}))\n"
                "print(json.dumps({'return': [\n"
                "    {'name': 'cross-model-dump'},\n"
                "    {'name': 'cross-model-address'},\n"
                "]}))\n"
                "print(\"Property 'virt-machine.__linx_cross_model_probe__' not found\", file=sys.stderr)\n",
            )
            result = self.run_preflight(binary, root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required property: cross-model-size", result.stderr.lower())

    def test_preflight_timeout_is_finite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            pid_file = Path(tmp) / "pid"
            binary = self.write_executable(
                root / "build-linx",
                "import os, pathlib, time\n"
                f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid()))\n"
                "time.sleep(30)\n",
            )
            started = time.monotonic()
            result = self.run_preflight(binary, root, timeout=0.5)
            elapsed = time.monotonic() - started
            pid = int(pid_file.read_text(encoding="utf-8"))
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timed out", result.stderr.lower())
        self.assertLess(elapsed, 2.0)

    def test_preflight_rejects_non_finite_timeout_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = self.write_executable(root / "build-linx", "raise SystemExit(1)\n")
            result = self.run_preflight(binary, root, timeout=float("inf"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timeout must be finite", result.stderr.lower())

    def test_preflight_accepts_controlled_recognition_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = self.write_executable(
                root / "build-linx",
                "import json, sys\n"
                "commands = [json.loads(line) for line in sys.stdin if line.strip()]\n"
                "if '-qmp' not in sys.argv or 'stdio' not in sys.argv:\n"
                "    raise SystemExit(2)\n"
                "if [item.get('execute') for item in commands] != ['qmp_capabilities', 'qom-list', 'quit']:\n"
                "    raise SystemExit(3)\n"
                "print(json.dumps({'QMP': {'version': {}}}))\n"
                "print(json.dumps({'return': {}}))\n"
                "print(json.dumps({'return': [\n"
                "    {'name': 'cross-model-dump'},\n"
                "    {'name': 'cross-model-address'},\n"
                "    {'name': 'cross-model-size'},\n"
                "]}))\n"
                "print(json.dumps({'return': {}}))\n",
            )
            result = self.run_preflight(binary, root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("recognized", result.stdout.lower())

    def test_preflight_rejects_binary_outside_qemu_root_build_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "qemu"
            binary = self.write_executable(Path(tmp) / "other", "raise SystemExit(0)\n")
            result = self.run_preflight(binary, root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match qemu root build target", result.stderr.lower())

    def test_provenance_has_literal_schema_and_deterministic_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ssm_sha = self.init_repo(root / "ssm", "ssm.txt")
            linx_sha = self.init_repo(root / "linx", "linx.txt")
            qemu_sha = self.init_repo(root / "qemu", "qemu.txt")
            artifacts = {}
            for name, content in {
                "qemu-bin": b"qemu-binary\n",
                "gfrun": b"gfrun-binary\n",
                "compiler": b"compiler\n",
                "linker": b"linker\n",
                "elf": b"elf\x00payload",
                "manifest": b'{"case":"v5"}\n',
            }.items():
                path = root / name
                path.write_bytes(content)
                artifacts[name] = path

            output_a = root / "provenance-a.json"
            output_b = root / "provenance-b.json"
            common_args = [
                "--ssm-root", str(root / "ssm"),
                "--linx-isa-root", str(root / "linx"),
                "--qemu-root", str(root / "qemu"),
                "--qemu-bin", str(artifacts["qemu-bin"]),
                "--gfrun-bin", str(artifacts["gfrun"]),
                "--compiler", str(artifacts["compiler"]),
                "--linker", str(artifacts["linker"]),
                "--elf", str(artifacts["elf"]),
                "--manifest", str(artifacts["manifest"]),
                "--models", "qemu,gfrun",
                "--pe-count", "4",
                "--linxisa-encoding-version", "v0.57",
                "--pto-isa-version", "v0.2",
                "--model-profile", "current-v0.2",
            ]
            for output in (output_a, output_b):
                result = subprocess.run(
                    [sys.executable, str(PROVENANCE), "--output", str(output), *common_args],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            self.assertEqual(output_a.read_bytes(), output_b.read_bytes())
            payload = json.loads(output_a.read_text(encoding="utf-8"))

        self.assertEqual(
            set(payload),
            {
                "schema_version",
                "repositories",
                "artifacts",
                "selected_models",
                "pe_count",
                "linxisa_encoding_version",
                "pto_isa_version",
                "model_profile",
            },
        )
        self.assertEqual(set(payload["repositories"]), {"superscalar_model", "linx_isa", "qemu"})
        self.assertEqual(payload["repositories"]["superscalar_model"]["sha"], ssm_sha)
        self.assertEqual(payload["repositories"]["linx_isa"]["sha"], linx_sha)
        self.assertEqual(payload["repositories"]["qemu"]["sha"], qemu_sha)
        self.assertFalse(payload["repositories"]["superscalar_model"]["dirty"])
        self.assertEqual(
            set(payload["artifacts"]),
            {"qemu_binary", "gfrun_binary", "compiler", "linker", "elf", "manifest"},
        )
        self.assertEqual(
            payload["artifacts"]["compiler"]["sha256"],
            hashlib.sha256(b"compiler\n").hexdigest(),
        )
        self.assertEqual(
            payload["artifacts"]["linker"]["sha256"],
            hashlib.sha256(b"linker\n").hexdigest(),
        )
        self.assertEqual(
            payload["artifacts"]["elf"]["sha256"],
            hashlib.sha256(b"elf\x00payload").hexdigest(),
        )
        self.assertEqual(payload["selected_models"], ["qemu", "gfrun"])
        self.assertEqual(payload["pe_count"], 4)
        self.assertEqual(payload["linxisa_encoding_version"], "v0.57")
        self.assertEqual(payload["pto_isa_version"], "v0.2")
        self.assertEqual(payload["model_profile"], "current-v0.2")

    def test_provenance_rejects_missing_selected_model_binary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for repo_name in ("ssm", "linx", "qemu"):
                self.init_repo(root / repo_name, repo_name + ".txt")
            artifact = root / "artifact"
            artifact.write_bytes(b"artifact")
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROVENANCE),
                    "--output", str(root / "out.json"),
                    "--ssm-root", str(root / "ssm"),
                    "--linx-isa-root", str(root / "linx"),
                    "--qemu-root", str(root / "qemu"),
                    "--qemu-bin", str(artifact),
                    "--compiler", str(artifact),
                    "--linker", str(artifact),
                    "--elf", str(artifact),
                    "--manifest", str(artifact),
                    "--models", "qemu,gfrun",
                    "--pe-count", "1",
                    "--linxisa-encoding-version", "v0.57",
                    "--pto-isa-version", "v0.2",
                    "--model-profile", "current-v0.2",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--gfrun-bin is required", result.stderr)

    def test_provenance_forces_tracked_untracked_and_ignored_submodule_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ssm = root / "ssm"
            linx = root / "linx"
            qemu = root / "qemu"
            self.init_repo(ssm, "ssm.txt")
            self.init_repo(linx, "linx.txt")
            self.init_repo(qemu, "qemu.txt")
            subsource = root / "subsource"
            self.init_repo(subsource, "sub.txt")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(qemu),
                    "-c",
                    "protocol.file.allow=always",
                    "submodule",
                    "add",
                    "-q",
                    str(subsource),
                    "sub",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(qemu),
                    "config",
                    "-f",
                    ".gitmodules",
                    "submodule.sub.ignore",
                    "all",
                ],
                check=True,
            )
            subprocess.run(["git", "-C", str(qemu), "add", ".gitmodules", "sub"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(qemu),
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-qm",
                    "add ignored submodule",
                ],
                check=True,
            )

            (ssm / "ssm.txt").write_text("tracked dirty\n", encoding="utf-8")
            (linx / "untracked.txt").write_text("untracked\n", encoding="utf-8")
            (qemu / "sub/sub.txt").write_text("submodule dirty\n", encoding="utf-8")

            artifact = root / "artifact"
            artifact.write_bytes(b"artifact")
            output = root / "provenance.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROVENANCE),
                    "--output", str(output),
                    "--ssm-root", str(ssm),
                    "--linx-isa-root", str(linx),
                    "--qemu-root", str(qemu),
                    "--qemu-bin", str(artifact),
                    "--compiler", str(artifact),
                    "--linker", str(artifact),
                    "--elf", str(artifact),
                    "--manifest", str(artifact),
                    "--models", "qemu",
                    "--pe-count", "1",
                    "--linxisa-encoding-version", "v0.57",
                    "--pto-isa-version", "v0.2",
                    "--model-profile", "current-v0.2",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))

        self.assertTrue(payload["repositories"]["superscalar_model"]["dirty"])
        self.assertTrue(payload["repositories"]["linx_isa"]["dirty"])
        self.assertTrue(payload["repositories"]["qemu"]["dirty"])

    def test_provenance_verification_rejects_changed_compiler_and_linker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for repo_name in ("ssm", "linx", "qemu"):
                self.init_repo(root / repo_name, repo_name + ".txt")
            artifact = root / "artifact"
            compiler = root / "custom-compiler"
            linker = root / "custom-linker"
            artifact.write_bytes(b"artifact")
            compiler.write_bytes(b"compiler-before")
            linker.write_bytes(b"linker-before")
            output = root / "provenance.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROVENANCE),
                    "--output", str(output),
                    "--ssm-root", str(root / "ssm"),
                    "--linx-isa-root", str(root / "linx"),
                    "--qemu-root", str(root / "qemu"),
                    "--qemu-bin", str(artifact),
                    "--compiler", str(compiler),
                    "--linker", str(linker),
                    "--elf", str(artifact),
                    "--manifest", str(artifact),
                    "--models", "qemu",
                    "--pe-count", "1",
                    "--linxisa-encoding-version", "v0.57",
                    "--pto-isa-version", "v0.2",
                    "--model-profile", "current-v0.2",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            failures = {}
            for name, path, original in (
                ("compiler", compiler, b"compiler-before"),
                ("linker", linker, b"linker-before"),
            ):
                path.write_bytes(name.encode() + b"-after")
                verify = subprocess.run(
                    [sys.executable, str(PROVENANCE), "--verify", str(output)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                failures[name] = verify
                path.write_bytes(original)
        for name, verify in failures.items():
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn(f"hash mismatch: {name}", verify.stderr.lower())

    def test_fail_closed_workflow_stops_before_runner_when_provenance_fails(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        match = re.search(r"```bash\n(# CURRENT_V02_GATE\n.*?)```", text, re.DOTALL)
        self.assertIsNotNone(match, "executable current-v0.2 gate block is missing")
        if match is None:
            return

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ssm = root / "ssm"
            linx = root / "linx"
            qemu = root / "qemu"
            skill = root / "skill"
            fake_bin = root / "bin"
            for directory in (ssm, linx, qemu, skill / "scripts", fake_bin):
                directory.mkdir(parents=True, exist_ok=True)
            (linx / "isa").mkdir()
            (qemu / "configure").write_text("marker\n", encoding="utf-8")
            (qemu / "build-linx").mkdir()
            (qemu / "build-linx/build.ninja").write_text("marker\n", encoding="utf-8")
            self.write_executable(qemu / "build-linx", "raise SystemExit(0)\n")
            (ssm / "build.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
            (ssm / "bin").mkdir()
            (ssm / "bin/gfrun").write_bytes(b"gfrun")
            (linx / "compiler/llvm/build-linxisa-clang/bin").mkdir(parents=True)
            (linx / "compiler/llvm/build-linxisa-clang/bin/clang++").write_bytes(b"clang")
            custom_tools = root / "custom-tools"
            custom_tools.mkdir()
            compiler = custom_tools / "non-default-clang++"
            linker = custom_tools / "non-default-ld.lld"
            compiler.write_bytes(b"custom compiler")
            linker.write_bytes(b"custom linker")
            compiler.chmod(compiler.stat().st_mode | stat.S_IXUSR)
            linker.chmod(linker.stat().st_mode | stat.S_IXUSR)

            cases = ssm / "tests/cross_model/cases"
            cases.mkdir(parents=True)
            generated = ssm / "tests/cross_model/generated"
            generated.mkdir()
            elf = generated / "fixture.elf"
            elf.write_bytes(b"elf")
            for name in ("v5_tile_smoke", "v5_shared_tma_smoke", "v5_group_mma_smoke"):
                (cases / f"{name}.json").write_text(
                    json.dumps(
                        {
                            "execution": {"pe_count": 1},
                            "isa": {"tile_profile": "davincioo-v5-superscalar"},
                        }
                    ),
                    encoding="utf-8",
                )
            build_args = root / "build-args.json"
            (ssm / "tests/cross_model/build_elf.py").write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                f"Path({str(build_args)!r}).write_text(json.dumps(sys.argv[1:]))\n"
                f"print({str(elf)!r})\n",
                encoding="utf-8",
            )
            runner_marker = root / "runner-invoked"
            (ssm / "scripts/cross_model").mkdir(parents=True)
            (ssm / "scripts/cross_model/run_diff.py").write_text(
                f"from pathlib import Path\nPath({str(runner_marker)!r}).write_text('invoked')\n",
                encoding="utf-8",
            )
            (skill / "scripts/preflight_qemu.py").write_text(
                "raise SystemExit(0)\n", encoding="utf-8"
            )
            (skill / "scripts/write_provenance.py").write_text(
                "raise SystemExit(23)\n", encoding="utf-8"
            )
            ninja = fake_bin / "ninja"
            ninja.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            ninja.chmod(ninja.stat().st_mode | stat.S_IXUSR)

            env = dict(
                os.environ,
                PATH=f"{fake_bin}:{os.environ['PATH']}",
                SSM_ROOT=str(ssm),
                LINX_ISA_ROOT=str(linx),
                QEMU_ROOT=str(qemu),
                QEMU_BIN=str(qemu / "build-linx/qemu-system-linx64"),
                SKILL_ROOT=str(skill),
                RUN_ID="failure-test",
                CLANGXX=str(compiler),
                LLD=str(linker),
            )
            result = subprocess.run(
                ["bash", "-c", match.group(1)],
                text=True,
                capture_output=True,
                timeout=10,
                check=False,
                env=env,
            )
            builder_arguments = json.loads(build_args.read_text(encoding="utf-8"))
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertFalse(runner_marker.exists())
        self.assertIn("--clangxx", builder_arguments)
        self.assertIn("--lld", builder_arguments)
        self.assertEqual(
            builder_arguments[builder_arguments.index("--clangxx") + 1], str(compiler)
        )
        self.assertEqual(builder_arguments[builder_arguments.index("--lld") + 1], str(linker))


if __name__ == "__main__":
    unittest.main()
