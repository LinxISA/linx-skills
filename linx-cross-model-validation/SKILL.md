---
name: linx-cross-model-validation
description: Run, diagnose, or extend Linx QEMU-to-gfrun architectural result validation using one ELF, manifest-defined memory segments, independent golden data, and structured reports. Use for cross-model ISA parity, Tile instruction result comparison, regression harness changes, mismatch triage, or coverage/status updates in SuperScalarModel.
---

# Linx Cross-Model Validation

Validate architecture-visible results. Do not treat matching logs, internal Tile
IDs, process exits, or two models failing in the same way as semantic agreement.

## Run the focused gate

1. Locate the `SuperScalarModel` checkout and inspect its Git status.
2. Ensure the matching QEMU branch contains the result-dump machine properties.
3. Build the models before interpreting failures:

```bash
python3 build.py configure --warnings-as-errors
python3 build.py build --target gfrun -j8
ninja -C ../linx-isa/emulator/qemu/build qemu-system-linx64
```

4. Run the comparator from the SuperScalarModel root:

```bash
python3 scripts/cross_model/run_diff.py
```

5. Read `summary.json` first, then the case `compare.json`. Inspect per-model
   stdout/stderr and traces only after locating the first architectural mismatch.

The initial case is `tests/cross_model/cases/tile_smoke.json`. It validates S32
row-major TLOAD/TSTORE and TADD over one 8x8 Tile.

## Preserve validation integrity

- Run the exact same ELF and initialized data on both models.
- Require QEMU to finish successfully before using it as a reference.
- Require each model to produce a complete result file. Missing, short, or long
  files are harness failures, not matching results.
- Compare QEMU, gfrun, and an independently generated golden result.
- Use the pass finisher at `0x10009000` value `0x5555` only as a termination
  protocol. Compare memory declared by the ELF symbol as the result oracle.
- Let the QEMU shutdown notifier dump memory after the finisher store retires.
- Keep unsupported selector/dtype/profile combinations fail-closed before
  destination mutation.
- Never compare internal physical Tile IDs; allocation policies can differ.
- Classify timeout, assertion, crash, unexpected trap, unsupported profile, and
  harness errors separately. Two failures never constitute PASS.

## Extend coverage

Keep assembly carriers coarse-grained by TMA, TEPL, or CUBE. Do not add one source
file per opcode.

For an exact integer profile:

1. Add the operation and a non-overlapping exported result segment to the
   consolidated carrier.
2. Add the segment's offset, byte size, dtype, shape, layout, comparison mode,
   and independent expected generator to its JSON manifest.
3. Rebuild through `tests/cross_model/build_elf.py`; never commit generated ELF,
   object, linker, report, or log artifacts.
4. Add runner self-tests when introducing a comparison mode or failure class.
5. Run `python3 -m unittest tests/cross_model/test_run_diff.py` and the real gate.
6. Update `docs/tile_instruction_status.md` only for the exact validated profile.

Do not silently apply floating-point tolerance. Add an explicit manifest mode
with documented NaN, signed-zero, absolute/relative error, and ULP policy first.

## Diagnose a failure

Use the report's first mismatch segment, byte offset, row, column, raw bits, and
typed value to select the next probe.

- If one process failed or timed out, debug decode/execution/termination before
  comparing bytes.
- If only gfrun differs, inspect canonical `BSTART` and `B.IOT` decoding before
  changing the test or golden data.
- If both models differ from golden in the same way, verify test initialization,
  address materialization, and the ISA contract; agreement alone is insufficient.
- If only QEMU differs, do not call it golden until its ISA profile and negative
  legality tests are confirmed.
- Use instruction traces as diagnostics after the architectural mismatch is
  known; do not require trace identity for PASS.

Keep QEMU and SuperScalarModel commits/PRs separate. Merge QEMU first, then update
the linx-isa QEMU gitlink to the upstream merge commit in a separate change.
