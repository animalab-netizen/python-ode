from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, Iterable, TypeVar

from .dto import EmptyOutput, ErrorOutput, Output, Outputs, ValueOutput
from .exceptions import GuardRejectedError

P = TypeVar("P")
R = TypeVar("R")
I = TypeVar("I")


@dataclass(frozen=True)
class GuardResult:
    is_allowed: bool
    error: Exception | None = None

    @classmethod
    def allow(cls) -> "GuardResult":
        return cls(True, None)

    @classmethod
    def deny(cls, error: Exception) -> "GuardResult":
        return cls(False, error)


@dataclass(frozen=True)
class ExecutionResult(Generic[R]):
    value: R | None = None
    output: Output[R] | None = None

    @property
    def is_output(self) -> bool:
        return self.output is not None

    @classmethod
    def from_value(cls, value: R) -> "ExecutionResult[R]":
        return cls(value=value, output=None)

    @classmethod
    def from_output(cls, output: Output[R]) -> "ExecutionResult[R]":
        return cls(value=None, output=output)


class UseCase(Generic[P, R]):
    async def process(self, param: P) -> Output[R]:
        guard = await self.guard(param)
        if not guard.is_allowed:
            return self.on_error(guard.error or GuardRejectedError("Guard rejected the dispatch."))

        try:
            execution = await self.execute(param)
            if execution.is_output:
                return execution.output  # type: ignore[return-value]
            return self.on_result(execution.value)  # type: ignore[arg-type]
        except Exception as error:
            return self.on_error(error)

    async def guard(self, param: P) -> GuardResult:
        return GuardResult.allow()

    async def execute(self, param: P) -> ExecutionResult[R]:
        raise NotImplementedError

    def on_result(self, result: R) -> Output[R]:
        return Outputs.value(result)

    def on_error(self, error: Exception) -> Output[R]:
        return Outputs.error(error)


class ChainUseCase(UseCase[P, R], Generic[P, I, R]):
    def __init__(
        self,
        first: UseCase[P, I],
        second: Callable[[I, P], Awaitable[ExecutionResult[R]]],
    ) -> None:
        self._first = first
        self._second = second

    async def execute(self, param: P) -> ExecutionResult[R]:
        first_output = await self._first.process(param)
        if isinstance(first_output, ValueOutput):
            return await self._second(first_output.value, param)
        if isinstance(first_output, ErrorOutput):
            return ExecutionResult.from_output(Outputs.error(first_output.error))
        if isinstance(first_output, EmptyOutput):
            return ExecutionResult.from_output(Outputs.empty())
        return ExecutionResult.from_output(Outputs.empty())


class SequenceUseCase(Generic[P, R]):
    def __init__(self, step: Callable[[P], Awaitable[R]]) -> None:
        self._step = step

    async def process(self, values: Iterable[P]) -> Output[list[R]]:
        ordered_values = list(values)
        if not ordered_values:
            return Outputs.empty()

        try:
            results: list[R] = []
            for value in ordered_values:
                results.append(await self._step(value))
            return Outputs.value(results)
        except Exception as error:
            return Outputs.error(error)


@dataclass(frozen=True)
class Unit:
    value: None = None


class UseCaseDispatcher:
    async def dispatch(
        self,
        param: P,
        use_case: UseCase[P, R],
        publish: Callable[[Output[R]], None] | None = None,
    ) -> Output[R]:
        output = await use_case.process(param)
        if publish is not None:
            publish(output)
        return output
