# UseCase Guide

Use `UseCase` when one request should produce one focused delivery.

Use `ChainUseCase` when a first successful delivery must contextualize the second step.

Use `SequenceUseCase` when execution order must remain explicit across three or more entries.

Use `GuardResult` and the `guard` hook when invalid dispatch must be rejected before I/O or state mutation begins.
