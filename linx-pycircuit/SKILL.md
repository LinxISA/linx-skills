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

## Workflow

1. Implement dialect/pass/frontend/backend change.
2. Rebuild generated artifacts and confirm producer scripts still conform.
3. Run PR mandatory pyCircuit gates.
4. If touched behavior affects LinxCore/trace, coordinate with `linx-core` + `linx-qemu`.
5. For nightly promotion, run nightly mandatory gates and publish evidence paths.

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
