---
name: linx-model
description: Cycle-accurate C++ model workflow for `tools/model`, including `SimQueue` payload policy, `Module` work semantics, port-role tagging, and queue wiring assertions. Use when adding or reviewing queue-wired model code.
---

# Linx Model

Canonical repo location (superproject checkout):

- `tools/model`

## Module work contract (strict)

- `Work()` is the one-cycle evaluation phase. A module reads current visible queue heads, performs combinational logic, and optionally enqueues results to output queues.
- Default rule: read at most one item per input queue and at most one item per inner queue per cycle unless the module spec explicitly requires multi-consume behavior.
- If a decision only needs to inspect data, use `Front()` and do not pop.
- Only consume when the module actually fires. Use `Read()` to transfer ownership/value out of the queue, or `Pop()` only after an intentional `Front()`-based decision.
- Do not mutate sibling-module state directly inside `Work()`. Cross-module communication must happen through `SimQueue`.
- `Xfer()` is not a substitute for datapath logic. Keep functional data motion in `Work()` and reserve `Xfer()` for phase-boundary bookkeeping if needed.

## Queue role discipline (strict)

- Parent modules own the real queue storage and pass only non-owning queue pointers to children.
- Distinguish three queue roles in module code:
  - `INPUT`: boundary queues driven from outside the module.
  - `OUTPUT`: boundary queues written by the module.
  - `INNER`: module-local/private queues used for internal pipelining or local observation.
- Do not overload `inputs_` to represent internal queues. If a module needs private readable queues, add a separate `inners_` container plus `AddInner()` / `Inner()` helpers before implementing the module logic.
- Do not wire one queue pointer into inconsistent roles in the same module without an explicit comment and assertion.

## Port binding macros (required pattern)

When writing module implementation files, bind queues through role-tagged macros or equivalent helper wrappers. The point is to make queue role visible in code review and fail fast on wiring mistakes.

```cpp
#define INPUT(name, idx) \
  auto* name [[maybe_unused]] = this->Input(idx); \
  LINX_MODEL_ASSERT(name != nullptr)

#define OUTPUT(name, idx) \
  auto* name [[maybe_unused]] = this->Output(idx); \
  LINX_MODEL_ASSERT(name != nullptr)

#define INNER(name, idx) \
  auto* name [[maybe_unused]] = this->Inner(idx); \
  LINX_MODEL_ASSERT(name != nullptr)
```

- If the framework already provides equivalent helpers, reuse them.
- If not, add the smallest helper layer needed before writing datapath code.
- Avoid raw repeated indexing such as `inputs_[0]` / `outputs_[1]` throughout `Work()`.

## Wiring and assertion rules (mandatory)

- In `Build()` / `BuildSelf()`, assert every queue pointer immediately after registration and connection.
- Assert expected port counts for modules with fixed interfaces.
- Prefer compile-time type equality on queue payloads when wiring templates across helpers.
- For `unique_ptr` payloads, ownership moves exactly once through `Write(std::move(...))` and `Read()`. Do not access the moved-from handle afterwards.
- For `shared_ptr` payloads, use sharing intentionally for observer/fanout cases; do not switch to `shared_ptr` just to avoid fixing ownership design.
- Use value payloads for flags, small integers, enums, and narrow tags.

## Work template

```cpp
void WorkSelf() override {
  INPUT(in0, 0);
  OUTPUT(out0, 0);
  // INNER(pipe0, 0);

  const bool fire = !in0->Empty() && !out0->Full();
  if (!fire) {
    return;
  }

  const auto& peek = in0->Front();
  if (!Accept(peek)) {
    return;
  }

  auto item = in0->Read();
  auto result = Combine(std::move(item));
  out0->Write(std::move(result));
}
```

- For value payloads, the same pattern applies with plain values:

```cpp
void WorkSelf() override {
  INPUT(flag_in, 0);
  OUTPUT(flag_out, 0);

  if (flag_in->Empty() || flag_out->Full()) {
    return;
  }

  const bool flag = flag_in->Read();
  flag_out->Write(!flag);
}
```

## Closeout line

- When this skill causes a material update, record:
  - `skill-evolve: update linx-model (module work + queue-role rules)`
