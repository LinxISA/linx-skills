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

Common env (when a TB enables runtime LinxTrace):

```bash
PYC_LINXTRACE=/abs/path/to/out.linxtrace
```

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
