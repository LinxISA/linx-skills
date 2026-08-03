---
name: linx-cross-model-validation
description: Run, diagnose, or extend Linx architectural result validation across QEMU, gfrun, and optionally gfsim using one ELF, manifest-defined memory segments, independent golden data, and structured reports. Use for cross-model ISA parity, Tile instruction result comparison, regression harness changes, mismatch triage, timing-model promotion, or coverage/status updates in SuperScalarModel.
---

# Linx Cross-Model Validation

Validate architecture-visible results. Do not treat matching logs, internal Tile
IDs, process exits, or two models failing in the same way as semantic agreement.

The superproject's pinned `tools/LinxCoreModel` is the canonical model closure.
An adjacent or otherwise external `SuperScalarModel` checkout supplies companion
diagnostic evidence only; it cannot replace that pinned closure for promotion
unless a separate governance change explicitly transfers ownership.

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

## Run the current PTO v0.2 gate

Execute the stages in this order: resolve paths, build, preflight, write
provenance, run the explicit v5 cases, then verify provenance again. Run the
following as one Bash block; `set -euo pipefail` makes every failed prerequisite
abort before the runner:

```bash
# CURRENT_V02_GATE
set -euo pipefail

SSM_ROOT="${SSM_ROOT:-$(git rev-parse --show-toplevel)}"
LINX_ISA_ROOT="${LINX_ISA_ROOT:-$(git -C "${SSM_ROOT}/../linx-isa" rev-parse --show-toplevel)}"
QEMU_ROOT="${QEMU_ROOT:-${LINX_ISA_ROOT}/emulator/qemu}"
QEMU_BIN="${QEMU_BIN:-${QEMU_ROOT}/build-linx/qemu-system-linx64}"
SKILL_ROOT="${SKILL_ROOT:?set SKILL_ROOT to linx-cross-model-validation}"
RUN_ID="${RUN_ID:?set a unique immutable run id}"
RESULTS_ROOT="${RESULTS_ROOT:-${SSM_ROOT}/regression_results/cross_model}"
CLANGXX="${CLANGXX:-${LINX_ISA_ROOT}/compiler/llvm/build-linxisa-clang/bin/clang++}"
LLD="${LLD:-${LINX_ISA_ROOT}/compiler/llvm/build-linxisa-clang/bin/ld.lld}"
MODELS="${MODELS:-qemu,gfrun}"

test -f "${SSM_ROOT}/build.py"
test -d "${LINX_ISA_ROOT}/isa"
test -f "${QEMU_ROOT}/configure"
SSM_ROOT=$(realpath "${SSM_ROOT}")
LINX_ISA_ROOT=$(realpath "${LINX_ISA_ROOT}")
QEMU_ROOT=$(realpath "${QEMU_ROOT}")
SKILL_ROOT=$(realpath "${SKILL_ROOT}")
export SSM_ROOT LINX_ISA_ROOT QEMU_ROOT QEMU_BIN SKILL_ROOT
export RUN_ID RESULTS_ROOT CLANGXX LLD MODELS
test -x "${CLANGXX}"
test -x "${LLD}"

(cd -- "${SSM_ROOT}" && env \
  SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
  QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
  python3 build.py configure --warnings-as-errors)
(cd -- "${SSM_ROOT}" && env \
  SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
  QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
  python3 build.py build --target gfrun -j8)

if [ ! -f "${QEMU_ROOT}/build-linx/build.ninja" ]; then
  mkdir -p "${QEMU_ROOT}/build-linx"
  (cd -- "${QEMU_ROOT}/build-linx" && env \
    SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
    QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
    "${QEMU_ROOT}/configure" --target-list=linx64-softmmu \
      --disable-docs --disable-werror)
fi
env SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
  QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
  ninja -C "${QEMU_ROOT}/build-linx" qemu-system-linx64
QEMU_BIN=$(realpath "${QEMU_BIN}")
export QEMU_BIN
test -x "${QEMU_BIN}"

case ",${MODELS}," in
  *,gfsim,*)
    (cd -- "${SSM_ROOT}" && env \
      SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
      QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
      python3 build.py build --target gfsim -j8)
    ;;
esac

python3 "${SKILL_ROOT}/scripts/preflight_qemu.py" "${QEMU_BIN}" \
  --qemu-root "${QEMU_ROOT}" --timeout 5

cases=(v5_tile_smoke v5_shared_tma_smoke v5_group_mma_smoke)
runner_cases=()
provenance_files=()
for case_name in "${cases[@]}"; do
  manifest="${SSM_ROOT}/tests/cross_model/cases/${case_name}.json"
  test -s "${manifest}"
  elf=$(cd -- "${SSM_ROOT}" && env \
    SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
    QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
    python3 tests/cross_model/build_elf.py \
      --case "cases/${case_name}.json" --linx-isa "${LINX_ISA_ROOT}" \
      --clangxx "${CLANGXX}" --lld "${LLD}")
  test -s "${elf}"
  pe_count=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["execution"]["pe_count"])' "${manifest}")
  model_profile=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["isa"]["tile_profile"])' "${manifest}")
  provenance="${RESULTS_ROOT}/${RUN_ID}/cases/${case_name}/provenance.json"
  python3 "${SKILL_ROOT}/scripts/write_provenance.py" \
    --output "${provenance}" \
    --ssm-root "${SSM_ROOT}" --linx-isa-root "${LINX_ISA_ROOT}" \
    --qemu-root "${QEMU_ROOT}" --qemu-bin "${QEMU_BIN}" \
    --gfrun-bin "${SSM_ROOT}/bin/gfrun" --gfsim-bin "${SSM_ROOT}/bin/gfsim" \
    --compiler "${CLANGXX}" --linker "${LLD}" \
    --elf "${elf}" --manifest "${manifest}" \
    --models "${MODELS}" --pe-count "${pe_count}" \
    --linxisa-encoding-version v0.57 --pto-isa-version v0.2 \
    --model-profile "${model_profile}"
  test -s "${provenance}"
  runner_cases+=(--case "${manifest}")
  provenance_files+=("${provenance}")
done

(cd -- "${SSM_ROOT}" && env \
  SSM_ROOT="${SSM_ROOT}" LINX_ISA_ROOT="${LINX_ISA_ROOT}" \
  QEMU_ROOT="${QEMU_ROOT}" QEMU_BIN="${QEMU_BIN}" \
  python3 scripts/cross_model/run_diff.py --no-build \
    --models "${MODELS}" --qemu "${QEMU_BIN}" \
    --gfrun "${SSM_ROOT}/bin/gfrun" --gfsim "${SSM_ROOT}/bin/gfsim" \
    --output "${RESULTS_ROOT}" --run-id "${RUN_ID}" "${runner_cases[@]}")

test -s "${RESULTS_ROOT}/${RUN_ID}/summary.json"
for provenance in "${provenance_files[@]}"; do
  python3 "${SKILL_ROOT}/scripts/write_provenance.py" --verify "${provenance}"
done
```

Do not assume `SuperScalarModel` is nested inside LinxISA. Require explicit
roots when discovery or marker checks fail. The block builds the exact
`build-linx/qemu-system-linx64` target and the preflight rejects any selected
binary that does not resolve to that target under `QEMU_ROOT`. QMP introspection
of `/machine` must list `cross-model-dump`, `cross-model-address`, and
`cross-model-size`; class help and property-order side effects are insufficient.

Historical runner defaults are not current PTO v0.2 evidence. Read
`summary.json` first, then each `compare.json`; inspect logs only after locating
the first architectural mismatch. A promotable case must retain its provenance.

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

This promotion applies only to the external companion lane. It does not promote
or repin the superproject's canonical `tools/LinxCoreModel` closure.

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
