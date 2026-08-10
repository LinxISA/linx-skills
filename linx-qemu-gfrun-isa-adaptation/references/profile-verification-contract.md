# Profile And Result Verification Contract

Use this reference when adding a profile binding, a state observation, or a
status/evidence update. Keep the contract machine-readable where the repository
already provides a generator; this document defines the semantic requirements.

## Result Observation

`tests/cross_model/build_elf.py` builds one test ELF with deterministic input
arrays. Resolve `cross_model_result` and `cross_model_result_size` from its symbol
table. Export that exact architecture-visible range from each model into an
isolated `result.bin` after the pass finisher retires.

The finisher at `0x10009000` with value `0x5555` is termination only. A natural
exit, decode success, retire log, internal Tile state, or finisher store does not
prove semantics. Treat missing, short, long, or late outputs as model/harness
failures.

## Binding

Every binding identifies one exact matrix cell and its evidence segments. For
example:

```json
{
  "opcode": "TLOAD",
  "profile": "Local S32; valid 4x8; declared layout=...; storage=...",
  "isa_ref": "v0.58",
  "segments": ["tload_s32_4x8"],
  "observations": ["tile:T#1"]
}
```

The profile string is descriptive, but the manifest must also carry structured
selector, dtype, shape, layout, storage, operand-role, and PE-count fields. A
binding that is not present in the current matrix catalog is an error; do not
invent an aggregate name to make a report pass.

## Evidence

Each promoted profile retains independent provenance and per-model results:

```json
{
  "opcode": "TEXPANDS",
  "profile": "U8; ...",
  "isa_commit": "<immutable commit>",
  "isa_ref": "v0.58",
  "verified_at": "YYYY-MM-DD",
  "manifest": "tests/cross_model/cases/v058_...json",
  "elf_sha256": "...",
  "golden": {"generator": "scripts/golden/...", "sha256": "..."},
  "models": {
    "qemu": {"result_sha256": "...", "run": {}},
    "gfrun": {"result_sha256": "...", "run": {}}
  },
  "pairwise": {"qemu_gfrun": true},
  "evidence_refs": {"segments": ["..."]}
}
```

For Tile-only effects, `observations` must identify the deterministic Tile or
architectural-register snapshot and its serialization. Memory evidence and Tile
state evidence are both architectural oracles; internal allocation IDs and trace
identity are not.

## Comparisons And Reports

Perform every selected golden and pairwise comparison:

```text
qemu  <-> golden      qemu  <-> gfrun
gfrun <-> golden      qemu  <-> gfsim
gfsim <-> golden      gfrun <-> gfsim
```

Use exact comparisons for integer/byte segments. An explicit floating-point
policy must state its bound and its NaN and signed-zero behavior. Report the
first mismatching segment, byte/element offset, row/column, raw bits, and typed
values. Classify timeout, assertion, crash, illegal trap, fail finisher, dump
error, incomplete output, golden mismatch, and harness error separately.

Expected case artifacts are `golden.bin`, `resolved_manifest.json`,
`compare.json`, `report.md`, `provenance.json`, and per-model `result.bin`, `run.json`,
`stdout.log`, and `stderr.log`. Reports are reproducibility evidence but remain
generated artifacts and must not be committed.

Generate provenance before running and verify it after running. It must record
resolved repository paths, SHAs, and dirty flags plus resolved paths and SHA-256
values for selected model binaries, compiler, linker, ELF, manifest, and golden
inputs. It also records selected models, PE count, ISA ref/commit, encoding
version, and exact profile. Do not promote evidence if any retained input changes.

## Promotion Invariants

- `PASS` requires current ISA provenance, a complete exact binding, independent
  golden equality for QEMU and gfrun, complete outputs, and required negative
  legality evidence.
- Evidence is profile-level. A shared carrier, opcode-level decoder coverage,
  or group MMA composition run cannot promote untested profiles.
- `--update` is transactional at the selected batch: if any profile is missing
  a model result, golden comparison, or binding, leave the status/evidence files
  unchanged and report the failure.
- `UNVERIFIED` is appropriate for stale/missing evidence or an unresolved
  timeout; `UNSUPPORTED` is for a defined tuple with a confirmed rejection or
  implementation defect; `N/A` is reserved for a profile not defined by the
  selected ISA.
- A pair of equal wrong outputs is a failed verification, never PASS.
