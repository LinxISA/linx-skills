# Cross-Stack Skills (Linux / LLVM / QEMU / libc)

## Linux

- Audit kernel objects for fused call headers and explicit return target setup.
- Use `tools/ci/check_linx_callret_crossstack.sh` as the primary shape gate.
- Treat `entry.S` and `switch_to.S` as pattern anchors.

## LLVM

- Keep musttail-first tail lowering on `FEXIT` path.
- Keep non-tail path on `FRET.STK`.
- Preserve call header adjacency and relocation legality in MC/codegen tests.

## QEMU

- Enforce strict call/ret contract traps by default.
- Validate dynamic targets are legal block starts.
- Preserve call-header sequence state across TB boundaries.
- Support all setret widths (`c.setret`, `setret`, `hl.setret`).

## musl / glibc

- Keep Linux UAPI-aligned ABI layouts (`setjmp`, signal, ucontext, ptrace/user regs).
- Eliminate fallback stubs for core arch paths (`clone`, restorer, sigsetjmp, unmapself, ldso hooks).
- Keep relocation contracts aligned across libc and linker (`R_LINX_*`).
