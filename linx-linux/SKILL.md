---
name: linx-linux
description: Linx Linux bring-up and runtime stabilization workflow. Use when debugging initramfs smoke/full boot failures, symbolizing trap loops, bisecting Linux+QEMU regressions, or validating kernel-side call/ret and block-target legality behavior.
---

# Linx Linux

## Overview

Use this skill for Linux runtime bring-up on Linx, from trap triage through stable smoke/full boot gates.

## Required runtime gates

```bash
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/initramfs/smoke.py
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/initramfs/full_boot.py
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/busybox_rootfs/boot.py
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linx_virt_defconfig_spec.py --defconfig /Users/zhoubot/linx-isa/kernel/linux/arch/linx/configs/linxisa_virt_defconfig --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/linxisa_virt_defconfig_audit.json
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
- regression rerun includes strict AVS system/runtime checks,
- timer IRQ behavior remains enabled in strict closure unless explicitly waived.

## Timer and BI-state diagnostics

- Distinguish signal-path success from timer-path success:
  `ctx_ri_step_trap_smoke.py` validates trap-resume (`BI=1` + restore);
  `ctx_tq_irq_smoke.py` validates timer-interrupt coverage.
- When diagnosing state corruption, use QEMU debug dump mode
  (`LINX_CPU_DUMP_DEBUG=1`) and inspect `EBARG/BSTATE` plus debug SSR
  (`DBCR/DBVR/DWCR/DWVR`) before and after trap return.
- Do not mark timer PASS if the only evidence is `mismatch==0` with
  `irq0_delta==0`; that is a non-covered path.

## Included scope

This consolidated skill absorbs prior `linux-bringup` and Linux-facing call/ret parity checks.

## References

- `references/runtime_triage.md`
