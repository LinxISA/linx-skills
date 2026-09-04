---
name: linx-pycircuit
description: pyCircuit and MLIR workflow for submodule `tools/pyCircuit`. Use when changing pyCircuit dialect, passes, compiler flows, or simulation pipelines, and when validating multi-.pyc build and integration behavior.
---

# Linx pyCircuit

## Overview

Use this skill for `tools/pyCircuit` development, flow validation, and integration checks against Linx bring-up lanes.

## Log / trace hygiene (strict)

- Avoid generating excessive large logs.
- Do not start broad pyCircuit/QEMU/LinxCore logging from the beginning of execution unless no narrower reproducer exists.
- First localize the point of interest, then enable only the minimum trace/log surface needed for that window.
- Keep artifacts bounded: smallest case set, shortest timeout, narrowest commit window, and no duplicate log streams unless they are required for correlation.
- Treat generated logs/traces as disposable debugging artifacts. Remove large outputs from `/tmp`, `/private/tmp`, and repo-local output trees once the needed evidence has been extracted.
- If a run is still producing logs after the needed evidence is captured, stop it before rerunning or widening the reproducer.

## Repository boundary (strict)

- `PTO-ISA/pyCircuit` owns reusable frontends, MLIR dialects/passes, runtimes,
  simulators, backends, generic examples, and framework gates.
- LinxCPU/LinxCore designs, ISA decoders, QEMU comparison, board files,
  product testbenches, and consumer trace adapters are owned by the Linx
  superproject or another consumer repository. Do not add them under the
  pyCircuit `integrations/`, `platforms/`, examples, tests, or runtime headers.
- Consumer compatibility gates run from the consumer checkout against an exact
  pyCircuit revision. The pyCircuit repository must not reach into a sibling
  Linx checkout or carry path-based exceptions for Linx sources.
- Route Linx consumer validation and cross-repository pin work through the
  `linx-superproject` workflow. This skill covers framework changes and the
  resulting consumer contract handoff, not consumer design implementation.

pyCircuit PR checks are deliberately lightweight. Required automation covers
repository/Python contracts; native, MLIR, runtime, or backend PRs add the
narrowest focused local evidence for their change.

```bash
pytest /Users/zhoubot/linx-isa/tools/pyCircuit/tests/unit -m unit
python3 /Users/zhoubot/linx-isa/tools/pyCircuit/tools/agentic-circuit/check-contracts.py
mkdocs build --strict
```

Full pyCircuit 6 closure is release-only and must complete before packages are
published:

```bash
PYC_GATE_RUN_ID=<run-id> bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_agentic_circuit.sh
python3 /Users/zhoubot/linx-isa/tools/pyCircuit/flows/tools/check_decision_status.py --status /Users/zhoubot/linx-isa/tools/pyCircuit/docs/gates/decision_status_v6.md --out /Users/zhoubot/linx-isa/tools/pyCircuit/.pycircuit_out/gates/<run-id>/decision_status_report.json --require-no-deferred --require-all-verified --require-concrete-evidence --require-existing-evidence
mkdocs build --strict
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_semantic_regressions_v6.sh
```

Examples gate now enforces strict decision coverage by default (`PYC_DECISION_STATUS_STRICT=1`).
Use a single run-id across example + semantic lanes for coherent evidence bundles:

```bash
PYC_GATE_RUN_ID=<run-id> PYC_DECISION_STATUS_STRICT=1 bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_examples.sh
```

## Release and nightly gates

```bash
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_examples.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims_nightly.sh
```

## Consumer interface rules (strict)

- Consumer repositories own their compatibility contract files and enforce
  version changes against pinned pyCircuit releases or commits.
- Breaking framework interfaces require the appropriate public package/ABI
  version change and migration notes in pyCircuit; consumer-specific schema
  identifiers do not become pyCircuit framework APIs.
- pyc6 is the only current product surface; Cycle-Aware Signal is a first-class architecture, not a compatibility layer.
- Decision 0013/0014 must remain enforced: runtime library packaging + STL-only default.
- Decision-complete semantic closure requires:
  - `.pyctrace` schema v3 (`PYC6TRC3`) with value/known/z payloads,
  - generated projects link `libpyc6_runtime`,
  - explicit invalidate/reset event stream with ordered pre-phase semantics,
  - full gate evidence without partial timeout acceptance.

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
3. Run the two lightweight PR checks and the focused test that proves the
   changed contract.
4. If behavior changes a published consumer contract, report the exact
   revision and required consumer-side follow-up; do not implement consumer
   design or comparison flows in pyCircuit.
5. For release promotion, run full AC/PYC closure; use nightly/manual lanes as
   diagnostic subsets only.
6. Archive closure evidence under `docs/gates/logs/<run-id>/` (commands, stdout/stderr, summary, decision mapping).
7. For long simulation lanes, use case-level controls:
   - `PYC_SIM_CASE_TIMEOUT_SEC`
   - `PYC_SIM_RETRY_ON_TIMEOUT`
   - `PYC_SIM_RESUME_FROM_CASE`
   - Case logs are split by lane: `docs/gates/logs/<run-id>/cases/run_sims/<case>/` and `.../cases/run_sims_nightly/<case>/`.
8. Prefer setting `PYC_GATE_RUN_ID` explicitly for every closure run so `run_examples.sh` and `run_semantic_regressions_v6.sh` land in the same evidence directory.

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
