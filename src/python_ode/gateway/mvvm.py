from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from python_ode.business.dto import Output
from python_ode.business.interactor import UseCase, UseCaseDispatcher

T = TypeVar("T")
P = TypeVar("P")
R = TypeVar("R")
TController = TypeVar("TController")


@dataclass(frozen=True)
class Channel(Generic[T]):
    name: str


class Subscription:
    def __init__(self, dispose: Callable[[], None]) -> None:
        self._dispose = dispose

    def dispose(self) -> None:
        self._dispose()


class BaseViewModel:
    def __init__(self) -> None:
        self._dispatcher = UseCaseDispatcher()
        self._observers: dict[str, list[Callable[[object], None]]] = {}

    def channel(self, name: str) -> Channel[T]:
        return Channel(name=name)

    def observe(self, channel: Channel[T], callback: Callable[[T], None]) -> Subscription:
        listeners = self._observers.setdefault(channel.name, [])
        listeners.append(callback)  # type: ignore[arg-type]

        def dispose() -> None:
            current = self._observers.get(channel.name, [])
            if callback in current:
                current.remove(callback)  # type: ignore[arg-type]

        return Subscription(dispose)

    def clear_observers(self) -> None:
        self._observers.clear()

    def publish(self, channel: Channel[T], output: T) -> None:
        for callback in list(self._observers.get(channel.name, [])):
            callback(output)  # type: ignore[arg-type]

    async def dispatch_use_case(
        self,
        param: P,
        use_case: UseCase[P, R],
        channel: Channel[Output[R]],
    ) -> Output[R]:
        return await self._dispatcher.dispatch(param, use_case, lambda output: self.publish(channel, output))


class Controller:
    pass


class ControllerFactory(Generic[TController]):
    def create(self) -> TController:
        raise NotImplementedError
