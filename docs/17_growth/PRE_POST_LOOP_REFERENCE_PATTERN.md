# Pre/Post Loop Reference Pattern (Local Sketch)

Reference pattern wording only:

- Sentinel pre-check -> AgentKit action -> post-execution accountability trail

This pattern is a local architecture sketch and not a live integration statement.

## Why this pattern

- pre-execution: decide whether an agent action should proceed
- execution: run action only if policy allows
- post-execution: record what happened for auditability/verification

## Safety boundaries

- no official AgentKit integration claim
- no Mycelium Trails integration claim
- no partnership claim
- no wallet execution/signing in this sketch
- regression evidence only, not a security guarantee
