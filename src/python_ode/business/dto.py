from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


class Output(Generic[T]):
    kind: str


@dataclass(frozen=True)
class ValueOutput(Output[T]):
    value: T
    kind: str = "value"


@dataclass(frozen=True)
class ErrorOutput(Output[T]):
    error: Exception
    kind: str = "error"


@dataclass(frozen=True)
class EmptyOutput(Output[T]):
    kind: str = "empty"


class Outputs:
    @staticmethod
    def value(value: T) -> ValueOutput[T]:
        return ValueOutput(value=value)

    @staticmethod
    def error(error: Exception) -> ErrorOutput[T]:
        return ErrorOutput(error=error)

    @staticmethod
    def empty() -> EmptyOutput[T]:
        return EmptyOutput()
