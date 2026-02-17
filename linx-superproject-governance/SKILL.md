---
name: linx-superproject-governance
description: Superproject governance for LinxISA root-to-leaf repository management. Use when changing submodule topology, syncing pinned and external lanes, updating submodule SHAs, enforcing root-only .gitmodules policy, or publishing reproducible gate evidence across llvm/qemu/linux/LinxCore/pyCircuit/glibc/musl.
---

# Linx Superproject Governance

## Overview

Use this skill to keep `/Users/zhoubot/linx-isa` reproducible: one root-level submodule map, no inter-leaf links, explicit dual-lane health, and gate status that always maps to a command plus SHA tuple.

## Invariants

- Keep LinxISA repo links only in `/Users/zhoubot/linx-isa/.gitmodules`.
- Keep leaf repos leaf-safe (no nested `.gitmodules` with `LinxISA/*` links).
- Keep canonical submodules: `compiler/llvm`, `emulator/qemu`, `kernel/linux`, `rtl/LinxCore`, `tools/pyCircuit`, `lib/glibc`, `lib/musl`.
- Keep `kernel/linux` `ignore=dirty` exception.
- Treat status markdown as a rendered view of machine-readable gate artifacts, not the source of truth.

## Governance workflow

1. Normalize topology and local config.

```bash
git submodule sync --recursive
git submodule update --init --recursive
bash tools/ci/check_repo_layout.sh
```

2. Run gate matrix in both lanes.
- Pin lane: exact submodule SHAs in superproject.
- External lane: active external worktrees/heads.

3. Record gate evidence atomically.
- Required fields per gate: command, lane, sha manifest, timestamp, result, artifact paths.
- Publish markdown from this artifact; do not manually edit outcomes.

4. Apply promotion rule.
- Promote external to pin only when required gates are green in both lanes or when defer policy is explicit.

## Topology cleanup tasks

- Remove non-root LinxISA URLs from nested `.gitmodules`.
- Deinit stale nested submodules under `.git/modules/...` when they are residue from old pins.
- Verify `git submodule status --recursive` has no unresolved nested LinxISA leaf entries.

## Failure triage

- `run_tests.sh --all` path synthesis errors: inspect repo-root derivation and include path checks.
- Docs claim green but rerun fails: treat docs as stale and regenerate from the gate artifact.
- Pin vs external mismatch: produce side-by-side lane report before any repin.

## References

- `references/topology_policy.md`
