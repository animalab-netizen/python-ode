from __future__ import annotations

from typing import Callable, TypeVar

from python_ode.business.dto import EmptyOutput, ErrorOutput, Output, ValueOutput

T = TypeVar("T")


def handle_output(
    output: Output[T],
    on_value: Callable[[T], None],
    on_error: Callable[[Exception], None],
    on_empty: Callable[[], None],
) -> None:
    if isinstance(output, ValueOutput):
        on_value(output.value)
        return
    if isinstance(output, ErrorOutput):
        on_error(output.error)
        return
    if isinstance(output, EmptyOutput):
        on_empty()
