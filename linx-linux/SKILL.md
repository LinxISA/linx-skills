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
python3 /Users/zhoubot/linx-isa/tools/bringup/check_linx_virt_defconfig_spec.py --defconfig /Users/zhoubot/linx-isa/kernel/linux/arch/linx/configs/linx_v150_defconfig --report-out /Users/zhoubot/linx-isa/docs/bringup/gates/linxisa_virt_defconfig_audit.json
```

For the merged direct-kernel recovery lane, these wrappers are firmwareless by
default. If you override `QEMU_EXTRA_ARGS`, preserve `-bios none` unless you
are explicitly testing a firmware artifact.

## Deterministic smoke repro

- For early boot triage, prefer the pinned `vmlinux` + initramfs smoke form so
  you can move the boot boundary without rebuilding QEMU each iteration:

```bash
TIMEOUT=20 LINX_DISABLE_TIMER_IRQ=1 SKIP_BUILD=1 \
QEMU=/Users/zhoubot/linx-isa/emulator/qemu/build/qemu-system-linx64 \
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/initramfs/smoke.py
```

- Keep the matching kernel rebuild command alongside it:

```bash
bash /Users/zhoubot/linx-isa/tools/bringup/run_linux_vmlinux_build_clean.sh \
  --linux-root /Users/zhoubot/linx-isa/kernel/linux \
  --out-dir /Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed \
  --clang /Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang \
  --gmake /opt/homebrew/bin/gmake \
  --target vmlinux
```

- Reproduce the current BusyBox rootfs lane with the clean helper path and
  explicit firmwareless boot when you need a rootfs-specific verdict instead of
  an initramfs-only boundary:

```bash
QEMU="$(bash /Users/zhoubot/linx-isa/tools/bringup/run_qemu_build_clean.sh \
  --qemu-root /Users/zhoubot/linx-isa/emulator/qemu \
  --out-dir /tmp/linx-qemu-clean-build \
  --target qemu-system-linx64)" \
SKIP_BUILD=1 QEMU="$QEMU" QEMU_EXTRA_ARGS='-bios none' \
python3 /Users/zhoubot/linx-isa/kernel/linux/tools/linxisa/busybox_rootfs/boot.py
```

- If the active `arch/linx` tree was replaced from a recovered authoritative
  patch and the clean build helper falls into Kconfig restart prompts, seed the
  build explicitly from the checked-in Linx defconfig before trying `vmlinux`:

```bash
cd /Users/zhoubot/linx-isa/kernel/linux
PATH=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin:$PATH \
/opt/homebrew/bin/gmake \
  O=/Users/zhoubot/linx-isa/kernel/linux/build-linx-fixed \
  ARCH=linx \
  LLVM=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/ \
  'CC=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang --target=linx64-unknown-linux-gnu -fintegrated-as' \
  HOSTCC=/usr/bin/clang HOSTCXX=/usr/bin/clang++ \
  linx_v150_defconfig olddefconfig
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
- treat `/chosen/bootargs` string corruption separately from later parser bugs:
  if the command line bytes are already wrong before `parse_args()`, fix the DT
  property read/import path first.
- Do not rely on a previously built `build-linx-fixed/vmlinux` after replacing
  `arch/linx` from a recovered patch. Rebuild from current source first; if the
  rebuild does not complete, treat runtime smoke results from the stale image as
  non-authoritative.

## Recovery-forward-port note

- When the Linux port is sourced from an older recovered patch, expect two
  independent classes of failures:
  - source/API drift against current kernel headers and MM helpers,
  - old Linx asm surface (`b.attr`, old block-head macros, unfused symbolic
    `BSTART CALL`, `%tpcrel_hi/%tpcrel_lo`) that depends on compiler-side
    compatibility.
- Separate those two before debugging runtime behavior: refresh the in-repo
  `clang` binary first when assembler/parser changes were made, then resume
  kernel source forward-porting.
- When the clean rebuild stops in the repeated
  `SelectionDAGISel::isOrEquivalentToAdd` crash family, use the generated
  `/var/folders/.../*.sh` Clang crash repro first. If removing the quoted cc1
  vectorizer flags makes the repro pass, prefer an object-scoped kernel
  workaround (`CFLAGS_<obj>.o += -fno-vectorize -fno-slp-vectorize`) before
  widening backend changes. Current verified progression moved through the
  earlier `fs/nfs`, `fs/lockd`, and `lib/random32.o` blockers and now stops
  later at `lib/hexdump.o`.

## Timer and BI-state diagnostics

- Distinguish signal-path success from timer-path success:
  `ctx_ri_step_trap_smoke.py` validates trap-resume (`BI=1` + restore);
  `ctx_tq_irq_smoke.py` validates timer-interrupt coverage.
- When diagnosing state corruption, use QEMU debug dump mode
  (`LINX_CPU_DUMP_DEBUG=1`) and inspect `EBARG/BSTATE` plus debug SSR
  (`DBCR/DBVR/DWCR/DWVR`) before and after trap return.
- Do not mark timer PASS if the only evidence is `mismatch==0` with
  `irq0_delta==0`; that is a non-covered path.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new kernel/runtime contract needed for stable closure,
  - new mandatory runtime gate/repro command/env,
  - new recurring trap/timer triage sequence.
- Skip updates for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-linux`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## Included scope

This consolidated skill absorbs prior `linux-bringup` and Linux-facing call/ret parity checks.

## References

- `references/runtime_triage.md`
