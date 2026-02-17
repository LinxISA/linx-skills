# Trap Triage

## High-priority symptom

Repeated trap loops at same PC (for example `pc=0x3166a0`) during `smoke.py` or `full_boot.py`.

## Procedure

1. Capture first repeating trap tuple: `pc`, `a`, cause, and nearest log context.
2. Symbolicate with `llvm-addr2line` on matching `vmlinux` build.
3. Disassemble neighborhood with `llvm-objdump`.
4. Determine if failure is:
- illegal branch target / block boundary issue,
- call/ret ABI mismatch,
- MMU/translation or fault-delivery bug.
5. Bisect Linux and QEMU SHAs.

## Exit criteria

- smoke and full boot both pass
- no repeated trap loop
- result captured in gate report with exact SHAs
