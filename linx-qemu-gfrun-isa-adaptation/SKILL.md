---
name: linx-qemu-gfrun-isa-adaptation
description: Adapt and validate PTO ISA Tile instruction profiles across QEMU, SuperScalarModel gfrun, and optionally gfsim using a pinned ISA source, current-encoding carriers, independent golden data, architectural-state observation, structured cross-model reports, and profile-level evidence/matrix updates. Use when implementing or debugging a PTO ISA instruction, running or extending the cross-model harness, diagnosing illegal/timeout/crash/mismatch results, promoting a profile to PASS, or maintaining QEMU/gfrun support workbooks.
---

# Linx PTO ISA Model Adaptation

Use this skill for the complete lifecycle of a clearly defined PTO ISA profile:
freeze the ISA contract, adapt QEMU and gfrun, run the same current-encoding ELF
against both models, compare architecture-visible observations with an independently
generated golden, and promote only exact profile cells with reproducible evidence.
Read `references/profile-verification-contract.md` before changing profile
bindings, result observation, comparison policy, artifacts, failure
classification, or status/evidence generation.

## 1. Establish Scope And Authority

1. Locate the four independent trees and read their nearest `AGENTS.md` files:
   `pto-spec` (or the user-selected ISA tree), `SuperScalarModel`,
   `linx-isa/emulator/qemu`, and the cross-repository `docs`/case directories.
   Inspect each repository's branch, `HEAD`, worktree, and remotes. Preserve
   existing user changes and never use an old worktree.
2. Require an explicit ISA ref and resolve it to an immutable commit before
   editing. The selected `pto-spec` tag/commit is the only semantic authority.
   Record the ref and commit in the run manifest and evidence. Do not silently
   mix pages from another tag. Before every verifier, importer, or generator
   invocation, require `git -C "$ISA_REPO" rev-parse "$ISA_REF"` to equal
   `ISA_COMMIT`. A version tag can lag the selected branch even when both are
   described informally as the same ISA release; a stale tag is not an alias
   for the selected immutable commit.
3. Read the instruction page and any referenced encoding/layout pages. Extract,
   without inference: opcode and block, mode/function selectors, operand order
   and count, dtype restrictions, PE-local shape/dimensions, Tile size and
   layout/storage, source/destination Tile roles, side effects, queue/rank rules,
   and illegal conditions. If a required definition is absent or contradictory,
   leave the profile `N/A`/`UNVERIFIED` with a page/index citation; do not guess.
4. Treat ISA v0.58 (or the ref supplied for the task) as current. Do not add or
   restore legacy decoder modes, accept a legacy ELF as current evidence, or
   make compatibility behavior a substitute for the selected current encoding.

## 2. Discover Repositories And Validation Binaries

Prefer explicit paths, then discover adjacent checkouts. Do not assume
`SuperScalarModel` is nested in `linx-isa`:

```bash
SSM_ROOT="${SSM_ROOT:-$(git rev-parse --show-toplevel)}"
LINX_ISA_ROOT="${LINX_ISA_ROOT:-$(git -C "${SSM_ROOT}/../linx-isa" rev-parse --show-toplevel)}"
QEMU_ROOT="${QEMU_ROOT:-${LINX_ISA_ROOT}/emulator/qemu}"
QEMU_BIN="${QEMU_BIN:-${QEMU_ROOT}/build-linx/qemu-system-linx64}"
```

If discovery fails, require the caller to provide the path. Resolve selected
paths with `realpath` and verify repository/binary markers such as `build.py`,
`target/linx`, and `qemu-system-linx64`. A stale binary is a harness error, not
ISA evidence.

Preflight QEMU's result transport before interpreting a model result. Query the
live `/machine` instance through QMP `qom-list` and require
`cross-model-dump`, `cross-model-address`, and `cross-model-size` in its returned
property names. Do not infer recognition from `virt,help`, QDict application
order, or an error on a later deliberately invalid property. Dynamic instance
properties may be absent from class help, and QDict hash order can report a
later error before an earlier missing requirement. Require `QEMU_BIN` to resolve
exactly to the binary built under the selected `QEMU_ROOT`.

## 3. Inspect Before Editing

Check the decoder tables, operand binding, handler, Tile state representation,
queue/fence/finisher path, and tests in both models. A decoder or handler being
present is not support evidence. First determine whether a timeout is caused by
the carrier/runner/ELF (wrong `BSTART`, rank/hand, operand binding, missing
finisher, queue progress) or by execution semantics. Preserve a minimal reproducer
and collect a bounded trace only after locating the first architectural event.

Keep implementation changes in the owning repository. QEMU and SuperScalarModel
are separate Git repositories and must have separate commits; do not modify
gfsim unless explicitly requested. Do not commit generated ELFs, object files,
logs, traces, or regression reports.

## 4. Implement The Current ISA Contract

1. Adapt the QEMU decoder and handler from the pinned ISA definition. Validate
   every selector, dtype, shape, layout, storage class, and operand before any
   destination, ACC, queue, Tile, or memory mutation. Unsupported or illegal
   tuples must fail closed: report an illegal instruction/trap and terminate the
   test protocol rather than waiting forever.
2. Adapt gfrun's canonical decoder/handler to the same contract and architectural
   state transitions. Keep instructions sequentially observable and decoupled:
   each instruction updates only the state and memory specified by the ISA;
   later instructions consume that committed architectural state.
3. Use a consolidated carrier for a family (TMA, TEPL, or CUBE), not one source
   file per opcode. A carrier may contain several non-overlapping segments, but
   each profile binding must identify the exact instruction tuple it proves.
4. Respect PE-local quantities. For cooperative four-PE operations, the logical
   group tile is the sum of four local tiles, while each instruction operand and
   TSize/shape value is the single-PE value required by the ISA. Do not expand a
   local value to a group value in an encoding or handler.
5. Treat explicit operands as explicit. For example, `TMATMUL.ACC` consumes ISA
   C and D operands; an implementation's implicit accumulator is not an ISA
   substitute. `TMATMUL` does not consume `PadValue` unless its page says so.
   `B.DATR` layout follows the declared ELF/ISA layout; never apply an
   unconditional `NZ2ND` conversion.

## 5. Build Independent Evidence

1. Build one ELF with deterministic initialized inputs. Resolve the result range
   from its `cross_model_result` and `cross_model_result_size` symbols instead of
   duplicating a guest address or size in the manifest. Run each model in an
   isolated artifact directory and export that model's own complete result only
   after a passing finisher.
2. Generate golden bytes/state independently of both models (for example from a
   small reference calculation or a checked-in generator). Never derive golden
   data from QEMU, gfrun, their traces, or a model-to-model result.
3. Run the exact same current-ISA ELF and deterministic initialization on QEMU
   and gfrun. Use the cross-model runner's isolated output files and finisher
   protocol. Compare each model independently with golden and also generate the
   QEMU/gfrun pairwise comparison. Exit code zero, a pass finisher, matching
   traces, or matching wrong output is insufficient for PASS.
4. Partition memory results into typed, non-overlapping manifest segments. Use
   exact byte comparison for integer data. Never silently apply floating-point
   tolerance: define NaN, signed-zero, absolute/relative error, and ULP behavior
   in the manifest before accepting it.
5. Observe the architectural effect named by the ISA. Compare exported memory
   segments for externally visible writes. If an instruction only changes Tile
   state (for example a load into a Tile), export and compare the relevant Tile
   state snapshot using a deterministic observation hook. Do not mark a profile
   PASS merely because a later instruction makes the state visible.
6. Use the pass finisher store at `0x10009000` with value `0x5555` only as a
   termination protocol. It is not a result oracle. Missing, short, long, or
   late output is a model/harness failure, never a matching result.
7. For illegal tuples, add a negative test that proves fail-closed behavior and
   no observable mutation before the trap. A timeout is a failure to diagnose,
   not an alternate spelling of illegal; repair termination/queue handling before
   changing semantics.

## 6. Run The Cross-Model Gate

Build the selected models before interpreting failures. Configure QEMU only when
its build directory is absent:

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

Run the comparator from `SuperScalarModel` with explicit binaries:

```bash
python3 scripts/cross_model/run_diff.py \
  --qemu "${QEMU_BIN}" \
  --gfrun "${SSM_ROOT}/bin/gfrun" \
  --case tests/cross_model/cases/<manifest>.json
```

Read `summary.json` first, then the failed case's `compare.json`. Use the first
mismatch segment, byte/element offset, row/column, raw bits, and typed values to
choose the next probe. Inspect model stdout/stderr and bounded traces only after
the first architectural failure is known.

Store reproducible run artifacts below
`regression_results/cross_model/<run-id>/cases/<case>/`: `golden.bin`,
`resolved_manifest.json`, `compare.json`, `report.md`, and one directory per
model with `result.bin`, `run.json`, `stdout.log`, and `stderr.log`. Do not commit
these generated files.

Create a deterministic `provenance.json` before execution, then use the runner's
no-build mode so the hashed ELF and binaries are exactly what ran. Record at
least:

- resolved paths, Git SHAs, and dirty flags for the ISA, SuperScalarModel, LinxISA,
  and QEMU repositories;
- paths and SHA-256 values for every selected model binary, compiler, linker,
  ELF, manifest, and independent golden generator/output;
- selected models, PE count, ISA ref/commit, encoding version, and exact profile
  binding.

After execution, verify the retained provenance against repository state and
artifact hashes. A changed or missing input invalidates promotion.

## 7. Profile Binding And Promotion

Use one exact matrix cell per profile: opcode, selectors, dtype(s), PE-local
shape, layouts/storage, and source/destination roles. A multi-segment carrier may
prove one profile, or several explicitly listed profiles, but an aggregate/group
case cannot promote a single-instruction cell by implication. Group MMA cases are
composition regressions: retain them to prove the instruction sequence works, but
also run independent single-instruction profile evidence.

Run the repository's existing workflow from `SuperScalarModel` (adjust paths to
the selected checkout):

```bash
test "$(git -C "$ISA_REPO" rev-parse "$ISA_REF")" = "$ISA_COMMIT"
python3 build.py build --target gfrun -j8
ninja -C "$QEMU_ROOT/build-linx" qemu-system-linx64
python3 scripts/verify_tile_profiles.py \
  --qemu "$QEMU_ROOT/build-linx/qemu-system-linx64" \
  --gfrun bin/gfrun --isa-commit "$ISA_COMMIT" --isa-ref "$ISA_REF"
python3 scripts/generate_tile_profile_matrix.py --check \
  --qemu-output "$QEMU_ROOT/docs/linxisa/qemu_tile_profile_support.xlsx"
```

Treat the profile catalog, evidence, status snapshot, and workbooks as a
directed data flow, not four equivalent files:

```text
pto-spec catalog + tile_profile_evidence.json overrides
                         |
                         v
              tile_profile_status.json
                         |
                         v
        gfrun workbook + QEMU workbook
```

`docs/tile_profile_status.json` and both XLSX files are generated projections.
For a new implementation-specific exact profile, register the exact profile
string in the owning opcode's `extended_profiles` in
`docs/tile_profile_evidence.json`, then run `import_tile_profile_status.py`
against the pinned `ISA_REF`/`ISA_COMMIT` to create an `UNVERIFIED` catalog cell.
Do this before the read-only verification gate. Do not add a profile only to
`tile_profile_status.json`: the next import correctly discards such an orphaned
derived-only edit, even if a verification record for it already exists.

Use this order for a new profile:

1. Add the exact string to the persistent evidence override catalog without
   claiming `PASS`.
2. Assert `ISA_REF` resolves to `ISA_COMMIT`, import the status snapshot, and
   confirm the new QEMU/gfrun cells are `UNVERIFIED`.
3. Run the selected manifest without `--update`; inspect `summary.json` and
   `compare.json`, not only the command return code.
4. Run the same selected batch with `--update` only after the read-only gate is
   fully `PASS`.
5. Re-read JSON and assert the exact profile is present in
   `extended_profiles`, has a current-commit verification record, and is `PASS`
   for both models. Then regenerate/check both workbooks.

Use `--update` only after the complete selected batch passes all independent
golden and pairwise checks. The update must preserve profile-level records in
`docs/tile_profile_evidence.json` and `docs/tile_profile_status.json`, then
regenerate/check the QEMU and gfrun workbooks. Never bulk-promote all profiles
because a shared carrier or opcode passed. Successful `--update` output is not
itself proof that the intended matrix cell survived import: verify the
postconditions above. Compare the before/after status maps and reject unrelated
`PASS -> UNVERIFIED`, `PASS -> UNSUPPORTED`, profile removal, or ISA-source
changes. These usually indicate a stale import ref, a missing persistent
`extended_profiles` override, or unintended evidence pruning rather than a new
model regression.

Status meanings are strict:

- `PASS`: current ISA provenance, exact binding, independent golden, QEMU and
  gfrun outputs all complete and equal, and required negative tests pass.
- `UNVERIFIED`: implementation or a plausible carrier exists, but current
  independent evidence is missing, stale, incomplete, or a timeout has not been
  localized.
- `UNSUPPORTED`: the tuple is defined but either model deliberately rejects it
  or a confirmed implementation defect remains.
- `N/A`: the current ISA does not define the tuple/profile. Cite the source page.

## 8. Optional gfsim Parity

Keep QEMU/gfrun functional profile PASS separate from optional gfsim timing-model
parity. Pending gfsim coverage does not invalidate functional PASS.

1. Build gfsim only when requested: `python3 build.py build --target gfsim -j8`.
2. Run `model_smoke` first and prove scalar stores older than the pass finisher
   are visible in gfsim's exported architectural memory.
3. Export gfsim's own `SoftMemory`; never substitute state from its embedded
   gfrun/reference core.
4. Require QEMU, gfrun, and gfsim each to match independent golden and require
   every pairwise comparison to match.
5. If the finisher becomes visible before older memory effects, classify an
   ordering/termination model defect. Do not hide it with a fixed delay,
   artificial stop cycle, or reference-core output.

Diagnostic Tile checkpoints must be passive at architectural completion or
retirement: they must not enqueue requests, consume ports, affect arbitration,
stall retirement, or change cycles. Instrumented export instructions are useful
for functional localization but are not evidence for uninstrumented timing.

## 9. Diagnose And Report Failures

Classify the first failure using evidence, not model agreement:

- `ISA_UNDEFINED`: missing/contradictory spec; preserve `N/A` or `UNVERIFIED` and
  cite exact page/section.
- `STALE_ISA_ELF` or `CARRIER_ERROR`: encoding, PE-local shape, rank/hand,
  operand binding, layout, initialization, finisher, or manifest is not current.
- `QEMU_ERROR` / `GFRUN_ERROR`: one model rejects, traps, crashes, times out, or
  produces a wrong architectural state for a valid tuple. Include decoder,
  handler, queue and state evidence.
- `GOLDEN_MISMATCH`: a model completes but differs from independently generated
  bytes/state; matching model outputs do not waive this category.
- `HARNESS_ERROR`: missing/short result, stale binary, absent observation,
  transport/property failure, or report-generation error.

If gfsim exports stale/zero data, validate the finisher-to-older-memory commit
contract before blaming a Tile opcode. If only gfrun differs, inspect canonical
`BSTART` and `B.IOT` decoding. If only QEMU differs, do not use QEMU as golden.
If multiple models differ from golden identically, audit initialization, address
materialization, carrier encoding, and the ISA contract.

For every non-PASS result record ISA ref/commit, manifest and binding, ELF hash,
golden provenance/hash, model commands and hashes, first mismatch or trap, and
the exact next action. Update audit markdown with source indexes; do not hide
uncertainty behind a broad `UNSUPPORTED` label.

## 10. Final Gates

Before handoff or a commit in either leaf repository, run the focused unit tests,
the selected cross-model manifests, `git diff --check`, workbook `--check`, and
`unzip -t` on both workbooks. Also assert the exact promoted profile in the
status JSON and evidence JSON, verify both model states are `PASS`, and inspect
the status diff for unrelated downgrades or removals. A valid XLSX ZIP and a
passing generator `--check` prove file integrity/reproducibility, not that the
intended profile cell exists. Verify no generated artifacts or runaway
processes remain. Report branch and commit per repository, test
commands/results, status changes, blockers, and whether anything was pushed.
Keep QEMU and gfrun history separate; the QEMU workbook belongs in the QEMU leaf
history, while gfrun evidence/status/workbook belongs in SuperScalarModel.
Update a superproject gitlink only after the leaf change is reviewed.

## Reference

- `references/profile-verification-contract.md` - runner, observation,
  binding/evidence schema, comparison contract, and promotion invariants.
