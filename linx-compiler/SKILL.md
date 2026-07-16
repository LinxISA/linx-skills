---
name: linx-compiler
description: Linx compiler/backend workflow for LLVM and compile gates. Use when implementing or debugging Linx codegen/MC behavior, enforcing call/ret lowering contracts, running compile coverage suites, or validating object/relocation correctness.
---

# Linx Compiler

## Overview

Use this skill for all compiler-side work centered on `compiler/llvm` and AVS compile gates.

## Focus areas

- Target backend changes (TableGen/ISel/MC/asm/disasm).
- ABI and call/ret lowering correctness.
- Compile-only gate stability and coverage.

## Canonical checks

```bash
python3 /Users/zhoubot/linx-isa/tools/isa/gen_c_codec.py --spec /Users/zhoubot/linx-isa/isa/v0.56/linxisa-v0.56.json --out-dir /tmp/linxisa-llvm-codec-check
diff -q /tmp/linxisa-llvm-codec-check/linxisa_opcodes.h /Users/zhoubot/linx-isa/compiler/llvm/llvm/lib/Target/LinxISA/MCTargetDesc/linxisa_opcodes.h
diff -q /tmp/linxisa-llvm-codec-check/linxisa_opcodes.c /Users/zhoubot/linx-isa/compiler/llvm/llvm/lib/Target/LinxISA/MCTargetDesc/linxisa_opcodes.c
cd /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests && CLANG=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang TARGET=linx64-linx-none-elf OUT_DIR=/Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/out-linx64 ./run.sh
python3 /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/analyze_coverage.py --out-dir /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/out-linx64 --fail-under 100
cd /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests && CLANG=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang TARGET=linx32-linx-none-elf OUT_DIR=/Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/out-linx32 ./run.sh
python3 /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/analyze_coverage.py --out-dir /Users/zhoubot/linx-isa/avs/compiler/linx-llvm/tests/out-linx32 --fail-under 100
```

The codec parity check is the source-of-truth proof that LLVM MC tables are
generated from the live v0.56 ISA catalog. The coverage checks must cover
710/710 unique v0.56 mnemonics and audit all 746 instruction definitions with
`99_spec_decode` included. Coverage conclusions require a fresh `run.sh` using
Clang rebuilt from the current `compiler/llvm` HEAD; if the binary's reported
VCS revision is stale, classify existing analyzer output as provenance/audit
evidence rather than a source defect.

## Toolchain lane policy

- Pin lane defaults to in-repo binaries:
  - `CLANG=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang`
  - `LLD=/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/ld.lld`
- Use external toolchain paths only in external lane or explicit override.
- In reports, include lane + compiler path provenance so gate outcomes are
  reproducible.

## Call/ret compile contract

- enforce call-header adjacency,
- preserve `FENTRY + FRET.STK` normal path,
- keep `FENTRY + FEXIT` tail-transfer path legal,
- preserve relocation/template checks.

## SIMT recurrence contract

- Treat generic loop-carried recurrences as order-dependent. Only recurrence
  kinds with an explicitly supported `v.rd*` reduction plan may use grouped
  multi-lane lowering.
- In auto layout, lower a generic recurrence with `LB0=1` scalar replay. An
  explicit grouped request must reject with a stable legality reason rather
  than emitting independent per-lane recurrence states.
- Recurrence carrier loads/stores synthesized by the compiler are memory
  traffic even when the source IR has no load or store. A body containing
  synthesized `.brg` accesses must use `MSEQ`/`MPAR`, never tile-only
  `VSEQ`/`VPAR`.
- Gate constant-trip recurrences with both assembly and runtime evidence: lock
  the recurrence update token as the stored value, require zero-offset carrier
  access in scalar replay, and compare auto-mode output with scalar mode.

## Workflow

1. Implement backend change.
2. Add lit/FileCheck coverage.
3. Rebuild the actual in-repo `clang` binary when the change touches the
   assembler/parser/MC path, not just `llvm-mc`:

```bash
ninja -C /Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang clang -j10
```

4. Validate both standalone MC and integrated-assembler surfaces when the
   change affects assembly syntax, reloc spelling, or expression parsing.
   Do not treat `llvm-mc` success as sufficient proof for `.S` files compiled
   through Clang:

```bash
/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/llvm-mc -triple=linx64 -filetype=obj /tmp/probe.s -o /tmp/probe.o
/Users/zhoubot/linx-isa/compiler/llvm/build-linxisa-clang/bin/clang -target linx64-linx-none-elf -c /tmp/probe.s -o /tmp/probe-clang.o
```

5. For recurring kernel-forward-port crashes in
   `SelectionDAGISel::isOrEquivalentToAdd`, first use the emitted Clang crash
   repro script from `/var/folders/.../*.sh` and remove the quoted
   `"-vectorize-loops"` / `"-vectorize-slp"` cc1 flags in that reproducer. If
   the repro then passes, treat the failure as a candidate for an
   object-scoped kernel workaround (`CFLAGS_<obj>.o += -fno-vectorize
   -fno-slp-vectorize`) before widening LLVM backend changes.
6. When a Linx runtime trap maps into compiler-rt `__atomic_*` helpers, inspect
   the linked object before changing workload code. Current Linx lowering can
   route C11 atomics used inside compiler-rt (`__c11_atomic_*`) back to the same
   public `__atomic_*` symbols, producing self-recursion such as
   `__atomic_load_1 -> __atomic_load_1`. A valid bring-up fallback must compile
   `compiler-rt/lib/builtins/atomic.c` for `linx64-unknown-linux-musl` and show
   no `__atomic_*` or `__c11` self-recursive relocations in `llvm-objdump -r`;
   disassembly should show direct load/store bodies for
   `__atomic_load_{1,2,4,8}` until native Linx atomic lowering is implemented.
7. Keep active compatibility MC coverage out of `legacy-*` naming. Historical
   baselines may stay archived, but any still-supported syntax/reloc surface
   should live under normal compatibility-oriented test names.
8. Run both linx64 and linx32 compile/coverage gates.
9. Confirm no cross-stack call/ret regressions.
10. Handoff gate evidence to integration owner before repin.

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new backend contract/call-ret rule tied to v0.56 closure,
  - new mandatory compile gate/repro command/env,
  - new recurring compiler triage pattern that changed debug order.
- Skip updates for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, validate with:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-compiler`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## Included scope

This consolidated skill absorbs prior `llvm-backend` and compiler-side `call-ret-parity` workflows.

## References

- `references/compiler_checks.md`
- `references/v0.3_codegen_and_asm_contracts.md` (archive-only historical baseline; not an active v0.56 gate source)
