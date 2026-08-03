# Validation Contract

## Inputs and observation

`tests/cross_model/build_elf.py` builds one test ELF. Keep deterministic input
arrays in the ELF so QEMU, gfrun, and gfsim receive identical code, addresses,
and initial bytes.

The ELF declares `cross_model_result` and `cross_model_result_size`. Resolve
both from the symbol table instead of duplicating a guest address or total size
in the manifest. Run each model in an isolated artifact directory and export
that range to the model's own `result.bin` after a passing finisher.

The finisher at `0x10009000` with value `0x5555` is a termination protocol, not
the result oracle. A natural exit, pass finisher, decode success, retire log, or
internal Tile state does not establish semantic agreement by itself.

## Golden and comparisons

Partition the exported range into typed, non-overlapping JSON manifest
segments. Generate `golden.bin` independently from the documented operation
semantics and deterministic inputs. Perform all applicable comparisons:

```text
qemu  <-> golden      qemu  <-> gfrun
gfrun <-> golden      qemu  <-> gfsim
gfsim <-> golden      gfrun <-> gfsim
```

Use exact comparison for integer and byte segments. Use floating-point
tolerance only when the manifest explicitly selects a policy such as
`fp32_ulp` and supplies its bound. Report the first mismatching segment,
byte/element offset, row/column, raw bits, and typed values.

## Artifacts

Publish runs below
`regression_results/cross_model/<run-id>/cases/<case>/`:

- `golden.bin`, `resolved_manifest.json`, `compare.json`, and `report.md`;
- one directory per model containing `result.bin`, `run.json`, `stdout.log`,
  and `stderr.log`.

Treat missing, short, long, or late result files as harness/model failures.
Classify timeout, assertion, crash, fail finisher, dump error, result mismatch,
and harness error separately. Two models failing the same way never pass.

Every promotable case must include deterministic `provenance.json` with these
top-level keys: `schema_version`, `repositories`, `artifacts`,
`selected_models`, `pe_count`, `linxisa_encoding_version`, `pto_isa_version`,
and `model_profile`. `repositories` records the resolved path, Git SHA, and
dirty boolean for SuperScalarModel, LinxISA, and QEMU. `artifacts` records the
resolved path and SHA-256 for every selected model binary, the exact compiler,
the exact linker, the ELF, and the manifest. Pass those same compiler and linker
paths to `build_elf.py` through its supported `--clangxx` and `--lld` options.
Do not infer or omit fields for a clean run.
Generate provenance before execution and use the runner's no-build mode so the
hashed ELF is the ELF that ran. After the runner returns, verify the retained
provenance against the current repository states and artifact hashes; a changed
or missing input invalidates promotion.

Retain bounded `summary.json`, `compare.json`, `report.md`, `provenance.json`,
and the first-mismatch excerpt used for triage. Raw memory dumps, complete
stdout/stderr, and full traces are disposable local or CI artifacts. Never
commit those generated artifacts; publish them through bounded CI retention
only when diagnosis needs them.

Before running QEMU, query the live `/machine` instance through QMP `qom-list`
and require `cross-model-dump`, `cross-model-address`, and `cross-model-size` in
the returned property names. Do not infer recognition from QDict application
order or from a later deliberately invalid machine property: QDict hash order
can report that later property before an earlier missing requirement. Do not
rely only on `virt,help`, because dynamically added instance properties may be
absent from its class-property listing. A binary without all three properties
cannot publish the architectural result and is a harness/QEMU-head mismatch.
The selected binary must resolve exactly to
`QEMU_ROOT/build-linx/qemu-system-linx64`, the target built by this workflow.

## Checkpoints and model state

The current harness compares final architecture-visible memory. It does not
compare TileReg, ACC, GPR, instruction traces, or internal microarchitectural
state after every operation. Export Tile or ACC results through an
architecture-visible path, normally `TSTORE` or `ACCCVT` followed by `TSTORE`.

For functional localization, reserve one result segment per important
operation and export intermediate Tile results from the carrier. Those extra
stores consume modeled resources and change gfsim timing; do not use such a run
as evidence for an uninstrumented cycle count.

A non-perturbing checkpoint requires a passive observer at architectural
operation completion/retirement. It must not enqueue modeled requests, consume
ports, alter arbitration, stall retirement, or change model cycles. Retain the
final-memory comparison as the acceptance oracle even when diagnostic
checkpoint traces are available.

## ISA-version boundary

Run generated PTO ISA v0.2 cross-model ELFs with the model's default canonical
decoder. Use `--pto-v02 false` only for the repository's legacy v0.1 prebuilt
pass lists. Those lists are model-regression evidence, not the
QEMU-gfrun-gfsim result-comparison oracle.

The current PTO ISA v0.2 gate consists specifically of
`v5_tile_smoke.json`, `v5_shared_tma_smoke.json`, and
`v5_group_mma_smoke.json`. The historical unversioned runner defaults cannot be
used as current-v0.2 promotion evidence.

## Model ownership boundary

The LinxISA superproject owns its canonical model closure through the pinned
`tools/LinxCoreModel` gitlink. Results from an external SuperScalarModel
checkout are companion diagnostic evidence: useful for cross-checking QEMU and
for functional or timing localization, but never a substitute for validating
the pinned closure. Changing that ownership or allowing external results to
satisfy the canonical gate requires a separate governance change and gitlink
update; this workflow does neither.
