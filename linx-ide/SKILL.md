---
name: linx-ide
description: Linx tooling and observability workflow across emulator, RTL, pyCircuit, and Konata. Use when building debug pipelines, generating and validating traces, triaging renderer issues, or coordinating model/emulator/RTL alignment.
---

# Linx IDE

## Overview

Use this skill as the consolidated developer-tooling surface for Linx debug, observability, and model alignment.

## Owned areas

- emulator debug workflow (`linx` QEMU-like behavior),
- pyCircuit MLIR/tool flow,
- RTL observability integration,
- Konata trace generation/validation/renderer triage.

## pyCircuit PR mandatory gates

```bash
bash /Users/zhoubot/linx-isa/tools/pyCircuit/contrib/linx/flows/tools/run_linx_cpu_pyc_cpp.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/contrib/linx/flows/tools/run_linx_qemu_vs_pyc.sh
python3 /Users/zhoubot/linx-isa/tools/bringup/check_pycircuit_interface_contract.py --root /Users/zhoubot/linx-isa --strict
```

## pyCircuit nightly mandatory gates

```bash
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_examples.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims.sh
bash /Users/zhoubot/linx-isa/tools/pyCircuit/flows/scripts/run_sims_nightly.sh
```

## LinxTrace PR mandatory gates

```bash
python3 /Users/zhoubot/linx-isa/rtl/LinxCore/tools/linxcoresight/lint_trace_contract_sync.py
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_konata_sanity.sh
python3 /Users/zhoubot/linx-isa/tools/bringup/check_trace_semver_compat.py --root /Users/zhoubot/linx-isa --strict
```

## LinxTrace nightly mandatory gates

```bash
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_konata_dfx_pipeview.sh
bash /Users/zhoubot/linx-isa/rtl/LinxCore/tests/test_konata_template_pipeview.sh
```

## Synchronization rules

- Keep these touchpoints synchronized for trace contract changes:
  - `rtl/LinxCore/src/common/stage_tokens.py`
  - `rtl/LinxCore/tb/tb_linxcore_top.cpp`
  - `rtl/LinxCore/tools/trace/build_linxtrace_view.py`
  - `rtl/LinxCore/tools/linxcoresight/lint_linxtrace.py`
  - `rtl/LinxCore/tools/linxcoresight/lint_trace_contract_sync.py`
- Breaking trace changes require major version bump + compatibility validation.
- pyCircuit interface contract changes require versioned updates and migration notes.

## Standard tooling loop

1. reproduce on emulator or model,
2. gather commit/trace artifacts,
3. compare against RTL/model expectations,
4. localize first divergence,
5. rerun strict gates.

## Konata workflow

If structural validation passes but UI is wrong, debug parser/renderer/theme paths.

## Included scope

This consolidated skill absorbs prior `isa-emulator`, `mlir-pycircuit`, `rtl-development`, and Konata split skills.

## References

- `references/tooling_matrix.md`
- `references/v0.3_qemu_trap_contracts.md` (v0.3 TRAPNO/E_BLOCK encoding + reporting contracts for QEMU)
