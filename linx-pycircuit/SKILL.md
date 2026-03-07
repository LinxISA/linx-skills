---
name: linx-pycircuit
description: pyCircuit and MLIR workflow for submodule `tools/pyCircuit`. Use when changing pyCircuit dialect, passes, compiler flows, or simulation pipelines, and when validating multi-.pyc build and integration behavior.
---

# Linx pyCircuit

## Overview

Use this skill for `tools/pyCircuit` development, flow validation, and integration checks against Linx bring-up lanes.

## PR mandatory gates

```bash
bash /Users/zhoubot/linx-isa/tools/pyCircuit/contrib/linx/flows/tools/run_linx_cpu_pyc_cpp.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/contrib/linx/flows/tools/run_linx_qemu_vs_pyc.sh
python3 /Users/zhoubot/linx-isa/tools/bringup/check_pycircuit_interface_contract.py --root /Users/zhoubot/linx-isa --strict
python3 /Users/zhoubot/linx-isa/tools/bringup/check_trace_semver_compat.py --root /Users/zhoubot/linx-isa --strict
```

Hard-break closure gates (for pyc4.0 closure phases) are also mandatory:

```bash
python3 /Users/zhoubot/linx-isa/tools/pyCircuit/flows/tools/check_decision_status.py --status /Users/zhoubot/linx-isa/tools/pyCircuit/docs/gates/decision_status_v40.md --out /Users/zhoubot/linx-isa/tools/pyCircuit/.pycircuit_out/gates/<run-id>/decision_status_report.json --require-no-deferred --require-all-verified --require-concrete-evidence --require-existing-evidence
mkdocs build
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_semantic_regressions_v40.sh
```

Examples gate now enforces strict decision coverage by default (`PYC_DECISION_STATUS_STRICT=1`).
Use a single run-id across example + semantic lanes for coherent evidence bundles:

```bash
PYC_GATE_RUN_ID=<run-id> PYC_DECISION_STATUS_STRICT=1 bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_examples.sh
```

## Optional (deep) gates

Model diff suite (pyCircuit vs QEMU correlation; use when touching trace/commit semantics):

```bash
python3 /Users/zhoubot/linx-isa/tools/bringup/run_model_diff_suite.py --root /Users/zhoubot/linx-isa
```

## Nightly mandatory gates

```bash
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_examples.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims_nightly.sh
```

## Interface rules (strict)

- Contract file: `docs/bringup/contracts/pyc_linxcore_interface_contract.json`
- Breaking interface changes require `MAJOR` bump.
- Additive backward-compatible changes require `MINOR` bump.
- Unversioned breaking changes must fail the interface gate.
- pyc4 hard-break mode disallows legacy compatibility APIs/flags.
- Decision 0013/0014 must remain enforced: runtime library packaging + STL-only default.
- Decision-complete semantic closure requires:
  - `.pyctrace` schema v3 (`PYC4TRC3`) with value/known/z payloads,
  - explicit invalidate/reset event stream with ordered pre-phase semantics,
  - full gate evidence without partial timeout acceptance.

## LinxTrace v1 runtime writer (strict)

- Runtime LinxTrace output is a single uncompressed `*.linxtrace` (JSONL) with in-band META first record.
- Legacy split outputs are forbidden: `*.linxtrace.jsonl`, `*.linxtrace.meta.json`, `*.gz`.
- `PYC_LINXTRACE_GZ` is removed (no gzip writer/reader path).
- DFX occupancy for canonical pipeline stages must be emitted from the real owner module/stage boundary.
  Do not rebuild `W1/W2` or other residency from commit-edge sidecars in top-level glue.
- `debug_occ` / probe authoring must stay probe-only.
  Do not add architectural state, pipeline flops, commit-edge counters, or redirect/block sidecar logic in pyc modules just to satisfy trace.
  If trace needs edge/sequence/block lifecycle reconstruction, prefer TB/raw-trace post-processing over synthesizing trace-only hardware.

Common env (when a TB enables runtime LinxTrace):

```bash
PYC_LINXTRACE=/abs/path/to/out.linxtrace
```

- Keep trace schema SemVer separate from commit schema identifiers:
  - `LINX_TRACE_SCHEMA_VERSION` is the architectural trace compatibility version (`MAJOR.MINOR`, currently `1.0`).
  - `LINX_COMMIT_SCHEMA_ID` is the producer/consumer commit-bundle identifier (for example `LC-COMMIT-BUNDLE-V1`).
  - Do not alias one to the other in producer scripts; `check_trace_semver_compat.py` and `check_pycircuit_interface_contract.py` both enforce this split.

## Hierarchy discipline + emitted-cost gates (strict)

- Use `@const` for structural/template metadata: `ParamSet`, `ModuleFamilySpec`, `ModuleVectorSpec/MapSpec/DictSpec`, and any frozen structural object that participates in specialization reuse.
- Use `@function` only for inline pure combinational helpers. JIT now rejects `@function` bodies that instantiate modules, allocate state, or exceed inline complexity caps.
- Use `@module` for repeated reusable/stateful hardware. Naked repeated hierarchy built from handwritten loops must be promoted to module families plus `m.array(...)`.
- Hard emitted-cost gates are unconditional in `pycc`:
  - hottest emitted source `<= 15000`
  - hottest emitted module `<= 40000`
  - total emitted C++ cost `<= 700000`
- Cross-repo closure commands for hierarchy work:

```bash
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_pyc_hierarchy_discipline.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tools/generate/update_generated_linxcore.sh
```

- Practical hierarchy heuristic:
  - prefer recursive bank/lane slices over per-entry stateful modules when parent `eval` fanout becomes the dominant emitted TU cost.
  - if a consumer only needs aggregate slot state, redesign the interface around packed masks/buses instead of many scalar ports; medium-size instance caches can still become the hottest emitted TUs.
  - if a helper scans queue state across `depth * fields`, place that scan in the queue-owning module and export only the compact summary; otherwise parent-side instance cache helpers often become the hottest emitted C++ shards even when the scan itself is already in a child module.
  - if a state owner already has recursive hierarchy, keep read/query services inside that owner tree and export only compact query outputs; a separate top-level grouped query tree still forces the parent to re-fanout every owned field and can leave the hottest emitted `tick/eval` shard in the parent.
  - validate hotspot guesses against the emitted top-module MLIR: rank `pyc.instance` sites by total I/O count before refactoring, because standalone child-module size often mispredicts the true parent-side instance-cache blocker.

## Workflow

1. Implement dialect/pass/frontend/backend change.
2. Rebuild generated artifacts and confirm producer scripts still conform.
3. Run PR mandatory pyCircuit gates.
4. If touched behavior affects LinxCore/trace, coordinate with `linx-core` + `linx-qemu`.
5. For nightly promotion, run nightly mandatory gates and publish evidence paths.
6. Archive closure evidence under `docs/gates/logs/<run-id>/` (commands, stdout/stderr, summary, decision mapping).
7. For long simulation lanes, use case-level controls:
   - `PYC_SIM_CASE_TIMEOUT_SEC`
   - `PYC_SIM_RETRY_ON_TIMEOUT`
   - `PYC_SIM_RESUME_FROM_CASE`
   - Case logs are split by lane: `docs/gates/logs/<run-id>/cases/run_sims/<case>/` and `.../cases/run_sims_nightly/<case>/`.
8. Prefer setting `PYC_GATE_RUN_ID` explicitly for every closure run so `run_examples.sh` and `run_semantic_regressions_v40.sh` land in the same evidence directory.

## Tooling reliability (common)

- If `git fetch` in the `tools/pyCircuit` submodule fails with `LibreSSL SSL_connect: SSL_ERROR_SYSCALL`, force Git to HTTP/1.1:

```bash
git -C /Users/zhoubot/linx-isa/tools/pyCircuit config http.version HTTP/1.1
```

- If `gh` GraphQL calls fail with `TLS handshake timeout` / `EOF`, retry with:

```bash
GH_HTTP_TIMEOUT=300 gh <command>
```

## Skill evolve loop (mandatory closeout)

- At closeout, decide `skill-evolve: update` or `skill-evolve: no-update`.
- Update this skill only for material reusable findings:
  - new pyCircuit↔LinxCore interface contract rule,
  - new required gate/command/env for reproducible closure,
  - new recurring divergence triage path across pyCircuit/QEMU/LinxCore.
- Skip updates for minor optimization, wording cleanup, or one-off local workaround.
- If update is needed, edit only touched skill docs and run:
  - `python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/zhoubot/linx-isa/skills/linx-skills/linx-pycircuit`
  - `python3 /Users/zhoubot/linx-isa/skills/linx-skills/scripts/check_skill_change_scope.py --repo-root /Users/zhoubot/linx-isa/skills/linx-skills --base origin/main`

## References

- `references/flow_checks.md`
