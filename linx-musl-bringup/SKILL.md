---
name: linx-musl-bringup
description: Linx musl bring-up and runtime validation workflow. Use when building musl for Linx64, validating static and shared runtime behavior separately, triaging runtime panics/timeouts, and enforcing explicit gate policy for M1/M2/M3/R1/R2 outcomes.
---

# Linx musl Bring-up

## Overview

Use this skill to run musl bring-up with strict separation of static and shared runtime results and no ambiguous aggregate pass.

## Build gates

```bash
MODE=phase-b /Users/zhoubot/linx-isa/lib/musl/tools/linx/build_linx64_musl.sh
```

Expected outputs:
- `out/libc/musl/logs/phase-b-summary.txt`
- `out/libc/musl/logs/phase-b-m3-shared.log`

## Runtime gates (must split)

Static gate:
```bash
python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link static
```

Shared gate:
```bash
python3 /Users/zhoubot/linx-isa/avs/qemu/run_musl_smoke.py --mode phase-b --link shared
```

Combined policy:
- Global musl runtime is green only when static and shared are both green, or when defer policy is explicitly documented.

## Required artifacts

- `avs/qemu/out/musl-smoke/summary_static.json`
- `avs/qemu/out/musl-smoke/summary_shared.json`
- `avs/qemu/out/musl-smoke/summary.json` (derived/combined)

## Common failure signatures

- `runtime_timeout`
- `shared_runtime_kernel_panic`
- `*_runtime_block_trap`

Always preserve sample-level logs for each failing mode.

## References

- `references/static_shared_policy.md`
