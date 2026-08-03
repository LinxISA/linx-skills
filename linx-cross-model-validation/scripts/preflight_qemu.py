#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import signal
import subprocess
import sys
from pathlib import Path


REQUIRED_PROPERTIES = (
    "cross-model-dump",
    "cross-model-address",
    "cross-model-size",
)


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def probe(binary: Path, timeout: float) -> tuple[int, str, str]:
    commands = "\n".join(
        json.dumps(command, separators=(",", ":"))
        for command in (
            {"execute": "qmp_capabilities"},
            {"execute": "qom-list", "arguments": {"path": "/machine"}},
            {"execute": "quit"},
        )
    ) + "\n"
    process = subprocess.Popen(
        [
            str(binary),
            "-machine",
            "virt",
            "-S",
            "-display",
            "none",
            "-nodefaults",
            "-qmp",
            "stdio",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(input=commands, timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        raise TimeoutError(stdout + stderr) from None
    return process.returncode, stdout, stderr


def qmp_properties(output: str) -> set[str]:
    messages = []
    for line in output.splitlines():
        try:
            messages.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not any(isinstance(message, dict) and "QMP" in message for message in messages):
        raise ValueError("QMP greeting was not received")
    for message in messages:
        result = message.get("return") if isinstance(message, dict) else None
        if isinstance(result, list):
            return {
                item["name"]
                for item in result
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            }
    raise ValueError("QMP qom-list response was not received")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed probe for Linx cross-model QEMU transport properties."
    )
    parser.add_argument("qemu_bin", type=Path)
    parser.add_argument("--qemu-root", required=True, type=Path)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    binary = args.qemu_bin.expanduser()
    if not binary.exists():
        return fail(f"QEMU binary is missing: {binary}")
    if not binary.is_file() or not os.access(binary, os.X_OK):
        return fail(f"QEMU binary is not executable: {binary}")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        return fail("timeout must be finite and greater than zero")

    binary = binary.resolve()
    qemu_root = args.qemu_root.expanduser().resolve()
    expected = (qemu_root / "build-linx/qemu-system-linx64").resolve()
    if binary != expected:
        return fail(
            f"selected binary does not match QEMU root build target: "
            f"selected={binary} expected={expected}"
        )
    try:
        returncode, stdout, stderr = probe(binary, args.timeout)
    except TimeoutError:
        return fail(f"QEMU property probe timed out after {args.timeout:g} seconds")
    except OSError as exc:
        return fail(f"could not execute QEMU binary {binary}: {exc}")
    try:
        properties = qmp_properties(stdout)
    except ValueError as exc:
        excerpt = " ".join((stdout + " " + stderr).strip().split())[:240] or "<no output>"
        return fail(f"unrecognized probe response from selected executable: {exc}; {excerpt}")
    missing = [name for name in REQUIRED_PROPERTIES if name not in properties]
    if missing:
        return fail(f"missing required property: {missing[0]}")
    if returncode != 0:
        excerpt = " ".join(stderr.strip().split())[:240] or f"exit {returncode}"
        return fail(f"QEMU exited after QMP property introspection: {excerpt}")

    print(
        "ok: QEMU recognized cross-model-dump, cross-model-address, and cross-model-size"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
