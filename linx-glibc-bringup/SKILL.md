---
name: linx-glibc-bringup
description: Linx glibc porting and gate progression workflow. Use when building or debugging the Linx64 glibc fork, moving from partial configure/csu success to full shared libc.so readiness, and validating ABI/relocation alignment with Linux and musl.
---

# Linx glibc Bring-up

## Overview

Use this skill for staged glibc progression (`G1a` to `G1b`) while keeping ABI and relocation semantics aligned with Linux and musl.

## Gate ladder

- `G1a`: configure + `csu/subdir_lib` + basic CRT objects.
- `G1b`: full shared `libc.so` build gate with explicit pass/fail evidence.

## Canonical build command

```bash
bash /Users/zhoubot/linx-isa/lib/glibc/tools/linx/build_linx64_glibc.sh
```

Primary evidence:
- `out/libc/glibc/logs/summary.txt`
- `out/libc/glibc/logs/02-configure.log`
- `out/libc/glibc/logs/03-make.log`

## Runtime-readiness policy

- Keep `G1a` as partial and report it explicitly.
- Add and report `G1b` separately.
- Block green promotion if Linux runtime baseline is unstable.

## Alignment checks

- Syscall/trap entry matches Linx contract.
- Relocation numbering matches Linux UAPI and musl contract.
- `setjmp`/signal/ucontext behavior remains compatible across libc and kernel interfaces.

## References

- `references/gates.md`
