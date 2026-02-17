---
name: linx-linux-bringup
description: Linux bring-up and runtime stabilization for LinxISA. Use when debugging Linx kernel boot failures, initramfs smoke/full-boot regressions, trap loops, or cross-repo Linux/QEMU interactions that block runtime gates.
---

# Linx Linux Bring-up

## Overview

Use this skill to close Linux runtime regressions with deterministic triage, symbolication, and cross-repo bisecting.

## Canonical runtime gates

```bash
python3 /Users/zhoubot/linux/tools/linxisa/initramfs/smoke.py
python3 /Users/zhoubot/linux/tools/linxisa/initramfs/full_boot.py
```

Expected outcome: both gates reach required shell/marker checks with no repeating trap loop.

## Trap triage workflow

1. Capture first repeated trap line (`pc`, `a`, cause, panic context).
2. Symbolicate PC against `vmlinux`.

```bash
llvm-addr2line -e /Users/zhoubot/linux/build-linx-fixed/vmlinux 0x3166a0
```

3. Inspect corresponding instruction window.

```bash
llvm-objdump -d /Users/zhoubot/linux/build-linx-fixed/vmlinux | rg -n "3166a0|<symbol>"
```

4. Determine class:
- bad block target,
- ABI/call-ret mismatch,
- translation/state bug.

5. Bisect between known-good and failing SHAs in `/Users/zhoubot/linux` and `/Users/zhoubot/qemu`.

## Cross-stack checks

- Verify `RET/IND/ICALL` paths keep explicit `setc.tgt`.
- Verify call-header adjacency contracts still hold.
- Re-run AVS call-ret contracts after Linux fixes.

## Promotion rule

Do not promote Linux runtime status to green until both smoke and full boot pass in the same lane and environment used for reporting.

## References

- `references/trap_triage.md`
