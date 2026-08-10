---
name: linx-superproject
description: LinxISA v0.58 superproject governance for exact component pins, topology, cross-repo gates, workload routing, and reproducible release evidence.
---

# Linx Superproject

## Authority and topology

The root `.gitmodules` declares topology. The exact v0.58 identities are locked
in `docs/bringup/component-lock.v0.58.json`; a directory name or local checkout
is not a pin.

Required component surfaces include:

- `compiler/llvm`
- `emulator/qemu`
- `kernel/linux`
- `rtl/LinxCore`
- `tools/pyCircuit`
- `tools/Linx-TileOP-API`
- `lib/glibc` and `lib/musl`
- `workloads/pto_kernels`
- `skills/linx-skills`

`workloads/SuperNPUBench` is forbidden as a standalone gitlink. Its maintained
v0.58 workload source lives under `workloads/pto_kernels/benchmarks/supernpu`.
Do not restore the old `PTO-Kernel` URL, the standalone SuperNPUBench pin, or
inter-leaf submodules.

## v0.58 architecture routing

- The execution engines are exactly `VEC`, `TLSU`, `CUBE`, and `SFU`.
- `TEPL` is the unchanged encoding carrier, not an engine. Use the v0.58
  `BSTART.VEC` and `BSTART.SFU` aliases without changing raw encodings.
- Linx-TileOP-API consumes the released LinxISA catalog. It must not invent
  selectors, revive deleted spellings, or silently choose an ambiguous form.
- PTO-kernels consumes Linx-TileOP-API and contains the nested SuperNPU flow.
  Its active sources may not use the pre-v0.58 embedded two-level API.
- The old AVS Tile/PTO parity sources are archive-only v0.57 evidence. They are
  not current v0.58 pass results. Track rebuilding them through the active
  repository issue instead of re-enabling them unchanged.

## Exact-pin discipline

1. Land and verify the leaf change first.
2. Record the merged leaf commit, tree, URL, branch, and role in the component
   lock.
3. Update the matching gitlink and no unrelated gitlinks.
4. Run topology, component, module, and documentation gates.
5. Review the exact superproject head, require hosted checks, squash with an
   exact head match, and prove the squash tree equals the reviewed tree.

If a leaf PR was squash-merged, pin the merged commit, never the topic head.
Never treat an external checkout or uncommitted worktree as release evidence.

## Required local gates

Run from the superproject root:

```bash
bash tools/ci/check_repo_layout.sh
python3 tools/ci/check_component_lock.py --root .
python3 -m unittest tools.ci.test_component_lock
make -C tools/Linx-TileOP-API check
python3 workloads/pto_kernels/scripts/check_supernpu_v058.py
python3 tools/isa/build_golden.py --profile v0.58 --check
python3 tools/isa/validate_spec.py --profile v0.58
python3 tools/isa/check_pto_v058_manifest.py --root .
python3 tools/isa/check_canonical_v058.py --root .
python3 tools/isa/check_agent_navigation.py --root .
python3 docs/check_documentation.py --root .
python3 tools/bringup/check_avs_contract.py
```

Run additional module/runtime gates when the changed surface requires them.
Pending, skipped, missing-tool, stale-SHA, or archived results cannot become a
pass. Preserve command, lane, exact SHA manifest, timestamp, outcome, and
artifact links for promoted evidence.

## AI workload flow

The active discovery root is nested SuperNPU in PTO-kernels. Use:

```bash
python3 tools/bringup/run_ai_workload_flow.py --profile smoke --list
python3 tools/bringup/run_ai_workload_flow.py --profile smoke --dry-run
```

The smoke inventory must resolve from the nested tree and use the separately
pinned Linx-TileOP-API. Do not route to deleted AVS parity suites or historical
standalone manifests. The first failing hard-break stage owns the fix; later
diagnostics cannot upgrade a blocked lane.

## Skills synchronization

Maintain skills through `$linx-skills-submodule`. After merging a material
skill update, repin `skills/linx-skills`, update the component lock, and install
the canonical copy:

```bash
bash skills/linx-skills/scripts/install_canonical_skills.sh
python3 skills/linx-skills/scripts/check_skill_change_scope.py \
  --repo-root skills/linx-skills --base origin/main
```

## Skill evolve closeout

Report either `skill-evolve: update linx-superproject (...)` or
`skill-evolve: no-update linx-superproject (...)`. Update only for reusable
topology, pin, gate, or workload-routing rules.

## References

- `references/runbook.md`
