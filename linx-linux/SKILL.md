---
name: linx-linux
description: Linx Linux bring-up and runtime stabilization workflow. Use when debugging initramfs smoke/full boot failures, symbolizing trap loops, bisecting Linux+QEMU regressions, or validating kernel-side call/ret and block-target legality behavior.
---

# Linx Linux

## Overview

Use this skill for Linux runtime bring-up on Linx, from trap triage through stable smoke/full boot gates.

## Canonical runtime gates

```bash
python3 /Users/zhoubot/linux/tools/linxisa/initramfs/smoke.py
python3 /Users/zhoubot/linux/tools/linxisa/initramfs/full_boot.py
```

## Trap triage

1. capture first repeated trap tuple (`pc`, cause, context),
2. symbolize with matching `vmlinux`,
3. disassemble neighborhood,
4. classify failure (target legality, ABI/call-ret, translation/fault),
5. bisect Linux/QEMU SHAs when needed.

## Cross-stack checks

- kernel call/ret path matches contract,
- dynamic targets are legal block starts,
- regression rerun includes strict AVS system/runtime checks.

## Included scope

This consolidated skill absorbs prior `linux-bringup` and Linux-facing call/ret parity checks.

## References

- `references/runtime_triage.md`
