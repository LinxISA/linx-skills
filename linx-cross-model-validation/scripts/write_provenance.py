#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


MODEL_BINARY_ARGS = {
    "qemu": "qemu_bin",
    "gfrun": "gfrun_bin",
    "gfsim": "gfsim_bin",
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "repositories",
    "artifacts",
    "selected_models",
    "pe_count",
    "linxisa_encoding_version",
    "pto_isa_version",
    "model_profile",
}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Write deterministic provenance for a cross-model result."
    )
    result.add_argument("--verify", type=Path)
    result.add_argument("--output", type=Path)
    result.add_argument("--ssm-root", type=Path)
    result.add_argument("--linx-isa-root", type=Path)
    result.add_argument("--qemu-root", type=Path)
    result.add_argument("--qemu-bin", type=Path)
    result.add_argument("--gfrun-bin", type=Path)
    result.add_argument("--gfsim-bin", type=Path)
    result.add_argument("--compiler", type=Path)
    result.add_argument("--linker", type=Path)
    result.add_argument("--elf", type=Path)
    result.add_argument("--manifest", type=Path)
    result.add_argument("--models")
    result.add_argument("--pe-count", type=int)
    result.add_argument("--linxisa-encoding-version")
    result.add_argument("--pto-isa-version")
    result.add_argument("--model-profile")
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def artifact(path: Path, label: str) -> dict[str, str]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"{label} is not a file: {resolved}")
    return {"path": str(resolved), "sha256": sha256(resolved)}


def git(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args],
            text=True,
            stderr=subprocess.PIPE,
        ).strip()
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or str(exc)
        raise ValueError(f"invalid Git repository {repo}: {detail}") from None


def repository(path: Path) -> dict[str, object]:
    resolved = path.expanduser().resolve()
    return {
        "path": str(resolved),
        "sha": git(resolved, "rev-parse", "HEAD"),
        "dirty": bool(
            git(
                resolved,
                "status",
                "--porcelain",
                "--untracked-files=normal",
                "--ignore-submodules=none",
            )
        ),
    }


def parse_models(raw: str) -> list[str]:
    models = [item.strip() for item in raw.split(",") if item.strip()]
    if not models:
        raise ValueError("--models must select at least one model")
    if len(models) != len(set(models)):
        raise ValueError("--models contains a duplicate model")
    unknown = [model for model in models if model not in MODEL_BINARY_ARGS]
    if unknown:
        raise ValueError(f"--models contains unsupported models: {', '.join(unknown)}")
    if "qemu" not in models:
        raise ValueError("--models must include qemu")
    return models


def verify(path: Path) -> None:
    provenance_path = path.expanduser().resolve()
    try:
        payload = json.loads(provenance_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid provenance JSON {provenance_path}: {exc}") from None
    if not isinstance(payload, dict) or set(payload) != TOP_LEVEL_KEYS:
        raise ValueError("provenance schema keys are incomplete or unexpected")
    if payload["schema_version"] != 1:
        raise ValueError(f"unsupported provenance schema version: {payload['schema_version']}")

    repositories = payload["repositories"]
    if not isinstance(repositories, dict) or set(repositories) != {
        "superscalar_model",
        "linx_isa",
        "qemu",
    }:
        raise ValueError("provenance repository set is incomplete or unexpected")
    for name, recorded in repositories.items():
        if not isinstance(recorded, dict) or set(recorded) != {"path", "sha", "dirty"}:
            raise ValueError(f"invalid repository record: {name}")
        current = repository(Path(recorded["path"]))
        if current != recorded:
            raise ValueError(f"repository state mismatch: {name}")

    artifacts = payload["artifacts"]
    if not isinstance(artifacts, dict):
        raise ValueError("invalid artifacts record")
    models = parse_models(",".join(payload["selected_models"]))
    required_artifacts = {"compiler", "linker", "elf", "manifest"} | {
        f"{model}_binary" for model in models
    }
    if set(artifacts) != required_artifacts:
        raise ValueError("provenance artifact set is incomplete or unexpected")
    for name, recorded in artifacts.items():
        if not isinstance(recorded, dict) or set(recorded) != {"path", "sha256"}:
            raise ValueError(f"invalid artifact record: {name}")
        current_hash = sha256(Path(recorded["path"]))
        if current_hash != recorded["sha256"]:
            raise ValueError(f"artifact hash mismatch: {name}")


def main() -> int:
    argument_parser = parser()
    args = argument_parser.parse_args()
    try:
        if args.verify is not None:
            verify(args.verify)
            print(f"ok: provenance verified: {args.verify.expanduser().resolve()}")
            return 0
        required = {
            "output": args.output,
            "ssm-root": args.ssm_root,
            "linx-isa-root": args.linx_isa_root,
            "qemu-root": args.qemu_root,
            "qemu-bin": args.qemu_bin,
            "compiler": args.compiler,
            "linker": args.linker,
            "elf": args.elf,
            "manifest": args.manifest,
            "models": args.models,
            "pe-count": args.pe_count,
            "linxisa-encoding-version": args.linxisa_encoding_version,
            "pto-isa-version": args.pto_isa_version,
            "model-profile": args.model_profile,
        }
        missing = [f"--{name}" for name, value in required.items() if value is None]
        if missing:
            raise ValueError(f"required arguments missing: {', '.join(missing)}")
        models = parse_models(args.models)
        if args.pe_count <= 0:
            raise ValueError("--pe-count must be greater than zero")

        artifact_paths = {
            "qemu_binary": args.qemu_bin,
            "compiler": args.compiler,
            "linker": args.linker,
            "elf": args.elf,
            "manifest": args.manifest,
        }
        for model in models:
            argument = MODEL_BINARY_ARGS[model]
            path = getattr(args, argument)
            if path is None:
                raise ValueError(f"--{argument.replace('_', '-')} is required for model {model}")
            artifact_paths[f"{model}_binary"] = path

        payload = {
            "schema_version": 1,
            "repositories": {
                "superscalar_model": repository(args.ssm_root),
                "linx_isa": repository(args.linx_isa_root),
                "qemu": repository(args.qemu_root),
            },
            "artifacts": {
                name: artifact(path, name) for name, path in artifact_paths.items()
            },
            "selected_models": models,
            "pe_count": args.pe_count,
            "linxisa_encoding_version": args.linxisa_encoding_version,
            "pto_isa_version": args.pto_isa_version,
            "model_profile": args.model_profile,
        }
        output = args.output.expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
