---
name: linx-superproject
description: LinxISA superproject governance and cross-repo execution workflow. Use when managing submodule topology, dual-lane pin/external sync, AVS gate reproducibility, SHA manifest reporting, or workload matrix publication across llvm/qemu/linux/LinxCore/pyCircuit/glibc/musl.
---

# Linx Superproject

## Overview

Use this skill for root-level coordination in `/Users/zhoubot/linx-isa`: topology rules, lane sync, gate truth, and cross-stack reporting.

## Core policy

- Keep LinxISA links in root `.gitmodules` only.
- Keep no inter-leaf LinxISA submodule links.
- Keep required submodules in sync:
  - `compiler/llvm`
  - `emulator/qemu`
  - `kernel/linux`
  - `rtl/LinxCore`
  - `tools/pyCircuit`
  - `lib/glibc`
  - `lib/musl`

## Canonical sync commands

```bash
git submodule sync --recursive
git submodule update --init --recursive
bash tools/ci/check_repo_layout.sh
```

## Dual-lane governance

- Pin lane: superproject submodule SHAs.
- External lane: active external trees.
- Run same gate matrix on both lanes and publish side-by-side outcomes.

## Gate truth contract

Always record for each gate:
- command,
- lane,
- SHA manifest,
- timestamp,
- pass/fail,
- artifact links.

Treat markdown status pages as generated views, not source-of-truth.

## Included scope

This consolidated skill owns:
- AVS gate orchestration,
- submodule topology cleanup,
- workload matrix publishing (including TSVC).

## References

- `references/runbook.md`
