---
name: linx-cross-model-validation
description: Run, diagnose, or extend Linx architectural result validation across QEMU, gfrun, and optionally gfsim using one ELF, manifest-defined memory segments, independent golden data, and structured reports. Use for cross-model ISA parity, Tile instruction result comparison, regression harness changes, mismatch triage, timing-model promotion, or coverage/status updates in SuperScalarModel.
---

# Linx Cross-Model Validation

Validate architecture-visible results. Do not treat matching logs, internal Tile
IDs, process exits, or two models failing in the same way as semantic agreement.

## Comparison contract

- Run the exact same ELF and deterministic initialized data on every model.
- Resolve the result address and size from the ELF symbols
  `cross_model_result` and `cross_model_result_size`.
- Export each model's own architecture-visible memory into an isolated
  `result.bin` after a passing finisher.
- Compare every selected model with independently generated golden bytes and
  generate all available pairwise comparisons.
- Treat this as end-of-program result validation, not instruction lockstep or
  microarchitectural-state comparison.

Read `references/validation_contract.md` before changing result observation,
comparison policy, artifacts, checkpoints, or failure classification.

## Run the focused gate

1. Locate the `SuperScalarModel`, LinxISA, and QEMU checkouts and inspect their
   Git status. Prefer explicit paths, then discover common adjacent layouts:

```bash
SSM_ROOT="${SSM_ROOT:-$(git rev-parse --show-toplevel)}"
LINX_ISA_ROOT="${LINX_ISA_ROOT:-$(git -C "${SSM_ROOT}/../linx-isa" rev-parse --show-toplevel)}"
QEMU_ROOT="${QEMU_ROOT:-${LINX_ISA_ROOT}/emulator/qemu}"
QEMU_BIN="${QEMU_BIN:-${QEMU_ROOT}/build-linx/qemu-system-linx64}"
```

   Do not assume `SuperScalarModel` is nested inside `linx-isa`. If adjacent
   discovery fails, stop and require `SSM_ROOT`, `LINX_ISA_ROOT`, `QEMU_ROOT`,
   or `QEMU_BIN` explicitly. Resolve every selected path with `realpath` and
   verify its expected marker before building (`build.py`, `target/linx`, or
   `qemu-system-linx64`).

2. Preflight the QEMU validation transport before interpreting model results:

```bash
test -x "${QEMU_BIN}"
for property in \
  cross-model-dump=/tmp/linx-cross-model-probe \
  cross-model-address=0 \
  cross-model-size=1
do
  output=$("${QEMU_BIN}" -machine "virt,${property}" \
    -S -display none -nodefaults 2>&1 || true)
  name=${property%%=*}
  if printf '%s\n' "${output}" | \
      grep -q "Property 'virt-machine.${name}' not found"; then
    printf 'missing QEMU machine property: %s\n' "${name}" >&2
    exit 1
  fi
done
```

   A missing property is a harness/QEMU-head mismatch, not an ISA result
   mismatch. `virt,help` is insufficient because these instance properties are
   added dynamically and may not appear in its class-property list. Rebuild the
   matching QEMU checkout or select the correct binary when the probe fails.

3. Build QEMU and the functional model before interpreting failures. Use the
   current `build-linx` directory by default; configure it only when absent:

```bash
cd "${SSM_ROOT}"
python3 build.py configure --warnings-as-errors
python3 build.py build --target gfrun -j8

if [ ! -f "${QEMU_ROOT}/build-linx/build.ninja" ]; then
  mkdir -p "${QEMU_ROOT}/build-linx"
  (cd "${QEMU_ROOT}/build-linx" && \
    "${QEMU_ROOT}/configure" --target-list=linx64-softmmu \
      --disable-docs --disable-werror)
fi
ninja -C "${QEMU_ROOT}/build-linx" qemu-system-linx64
```

   Build gfsim only when it is selected for the three-model lane:

```bash
python3 build.py build --target gfsim -j8
```

4. Run the comparator from the SuperScalarModel root and pass the resolved
   binaries when they are not at the runner defaults:

```bash
python3 scripts/cross_model/run_diff.py \
  --qemu "${QEMU_BIN}" \
  --gfrun "${SSM_ROOT}/bin/gfrun"
```

5. Read `summary.json` first, then the case `compare.json`. Inspect per-model
   stdout/stderr and traces only after locating the first architectural mismatch.

The default gate remains QEMU-gfrun and uses consolidated TMA, TEPL, and CUBE
cases. Select gfsim explicitly only when promoting an adapted profile to
timing-model parity:

```bash
python3 scripts/cross_model/run_diff.py \
  --models qemu,gfrun,gfsim \
  --qemu "${QEMU_BIN}" \
  --gfrun "${SSM_ROOT}/bin/gfrun" \
  --gfsim "${SSM_ROOT}/bin/gfsim" \
  --case tests/cross_model/cases/model_smoke.json
```

## Preserve validation integrity

- Run the exact same ELF and initialized data on every selected model.
- Require QEMU to finish successfully before using it as a reference.
- Require each model to produce a complete result file. Missing, short, or long
  files are harness failures, not matching results.
- Compare every selected model independently with golden and generate all
  available pairwise comparisons.
- Use the pass finisher at `0x10009000` value `0x5555` only as a termination
  protocol. Compare memory declared by the ELF symbol as the result oracle.
- Let the QEMU shutdown notifier dump memory after the finisher store retires.
- Keep unsupported selector/dtype/profile combinations fail-closed before
  destination mutation.
- Never compare internal physical Tile IDs; allocation policies can differ.
- Classify timeout, assertion, crash, unexpected trap, unsupported profile, and
  harness errors separately. Two failures never constitute PASS.
- Keep generated PTO ISA v0.2 cross-model ELFs on the model default canonical
  decoder. `--pto-v02 false` is only for the repository's legacy v0.1 prebuilt
  pass lists; those pass lists are model regression evidence, not the
  QEMU-gfrun-gfsim result-comparison oracle.

## Promote to gfsim parity

Keep QEMU-gfrun functional adaptation and three-model timing parity as separate
status levels. Pending gfsim parity does not invalidate an established
QEMU-gfrun result.

1. Run `model_smoke` first. It must prove that scalar stores older than the pass
   finisher are visible in gfsim's exported architectural memory.
2. Export gfsim's own `SoftMemory`; never substitute state from its embedded
   gfrun/reference core.
3. Require QEMU, gfrun, and gfsim each to match the independent golden result,
   and require all three pairwise comparisons to match.
4. After `model_smoke` passes, run the relevant consolidated TMA, TEPL, or CUBE
   carrier before promoting an instruction profile.

A successful decode, natural exit, pass finisher, retire log, internal Tile
state, or prebuilt ELF pass-list is diagnostic evidence only. In particular, a
pass finisher may be observed before architecturally older memory effects reach
the exported memory. Classify that as an ordering/termination model gap; do not
hide it with an artificial stop cycle, a fixed post-finisher delay, or
reference-core output.

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
- If gfsim exits successfully but exports stale or zero memory, first verify the
  finisher-to-older-memory commit contract with `model_smoke`; do not attribute
  the failure to a Tile opcode yet.
- If only gfrun differs, inspect canonical `BSTART` and `B.IOT` decoding before
  changing the test or golden data.
- If two or more models differ from golden in the same way, verify test
  initialization, address materialization, and the ISA contract; agreement
  alone is insufficient.
- If only QEMU differs, do not call it golden until its ISA profile and negative
  legality tests are confirmed.
- Use instruction traces as diagnostics after the architectural mismatch is
  known; do not require trace identity for PASS.

Keep QEMU and SuperScalarModel commits/PRs separate. Merge QEMU first, then update
the linx-isa QEMU gitlink to the upstream merge commit in a separate change.

## References

- `references/validation_contract.md`
