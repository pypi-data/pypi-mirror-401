from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    """栈"""

    def __init__(self) -> None:
        self._l: list[T] = []

    def pop(self) -> T | None:
        if self.empty:
            return None
        return self._l.pop()

    def push(self, item: T) -> None:
        self._l.append(item)

    @property
    def empty(self) -> bool:
        return len(self._l) == 0

    @property
    def size(self) -> int:
        return len(self._l)

    @property
    def peak(self) -> T | None:
        if self.empty:
            return None
        return self._l[-1]

    @property
    def data(self) -> list[T]:
        return self._l.copy()
