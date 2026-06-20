# python-ode

`python-ode` is the Python member of the ODE architecture family.

The package provides a compact runtime for:

- use case execution
- guard-first dispatch flow
- explicit output publication
- chained and sequenced orchestration
- lightweight MVVM-style channels for viewmodel driven UI code

## Repository

- source: [github.com/animalab-netizen/python-ode](https://github.com/animalab-netizen/python-ode)

## Status

`python-ode` is prepared as a standalone publishable package and is intended to be consumed by showcase applications such as `python-ode-consumer`.

The package is maintained by ÂnimaLab and is being positioned as the Python expression of the same ODE vocabulary already available in Kotlin, Swift, TypeScript and .NET.

## Coordinates

Current coordinates:

- package: `python-ode`
- version: `0.1.0`

Installation:

```bash
pip install python-ode
```

## Public API

The intended public surface of `python-ode` is centered on these concepts:

- `UseCase[P, R]`
- `UseCaseDispatcher`
- `Output`, `ValueOutput`, `ErrorOutput`, `EmptyOutput`, `Outputs`
- `BaseViewModel`
- `Channel`
- `Controller`
- `ControllerFactory`
- `SequenceUseCase`
- `ChainUseCase`
- `HttpError`, `ConnectionError`, `GuardRejectedError`, `UnexpectedResponseError`

Internal helpers should not be treated as product contract and may change without notice.

## Core Concepts

### 1. UseCase

`UseCase[P, R]` is the main business execution abstraction.

It provides a standard lifecycle for:

- input validation via `guard`
- execution via `execute`
- result normalization via `on_result`
- failure handling via `on_error`

### 2. Outputs

`python-ode` uses an explicit output hierarchy:

- `ValueOutput[T]`
- `ErrorOutput[T]`
- `EmptyOutput[T]`

### 3. ChainUseCase

`ChainUseCase` is intended for a two-step flow where the first successful result provides the context for the second step.

### 4. SequenceUseCase

`SequenceUseCase` is intended for ordered execution across three or more entries.

### 5. BaseViewModel

`BaseViewModel` provides:

- typed channel creation
- observation registration
- output publication through named channels
- direct use case dispatch into a chosen channel

## Basic Examples

### Direct UseCase

```python
from python_ode import ExecutionResult, UseCase


class LoadPokemonUseCase(UseCase[str, str]):
    async def execute(self, param: str) -> ExecutionResult[str]:
        return ExecutionResult.from_value(f"spotlight:{param}")
```

### Guarded UseCase

```python
from python_ode import ExecutionResult, GuardRejectedError, GuardResult, UseCase


class ComparePokemonUseCase(UseCase[tuple[str, str], str]):
    async def guard(self, param: tuple[str, str]) -> GuardResult:
        left, right = param
        if not left or not right or left == right:
            return GuardResult.deny(
                GuardRejectedError("Comparison requires two distinct pokemon.")
            )

        return GuardResult.allow()

    async def execute(self, param: tuple[str, str]) -> ExecutionResult[str]:
        left, right = param
        return ExecutionResult.from_value(f"{left} vs {right}")
```

## Publishing

Local validation:

```bash
python3 -m unittest discover /Users/caiosanchezchristino/Desktop/ode-projects/python-ode/tests
python3 -m pip wheel /Users/caiosanchezchristino/Desktop/ode-projects/python-ode --no-build-isolation --no-deps -w /tmp/python-ode-dist
```

See [PUBLICATION.md](/Users/caiosanchezchristino/Desktop/ode-projects/python-ode/PUBLICATION.md) for the release checklist and packaging notes.

## Contributing

See [CONTRIBUTING.md](/Users/caiosanchezchristino/Desktop/ode-projects/python-ode/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](/Users/caiosanchezchristino/Desktop/ode-projects/python-ode/CHANGELOG.md).

## Maintainer

- name: `ÂnimaLab`
- email: `animalab.desenvolvimento@gmail.com`

## License

This project is licensed under Apache-2.0. See [LICENSE](/Users/caiosanchezchristino/Desktop/ode-projects/python-ode/LICENSE).

## UseCase Guide

See [USECASE_GUIDE.md](/Users/caiosanchezchristino/Desktop/ode-projects/python-ode/USECASE_GUIDE.md) for combinations, adoption guidance and common implementation doubts.
