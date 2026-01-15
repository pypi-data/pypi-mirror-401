from typing import Iterable, Callable, Optional, TypeVar, List

T = TypeVar("T")
B = TypeVar("B")


def first_or_raise(list_: List[T]) -> T:
    if len(list_) == 0:
        raise IndexError("Attempted to retrieve first element of an empty list.")
    return list_[0]


def first_or_none(iterable: Iterable[T], predicate: Callable[[T], bool] = lambda _: True) -> Optional[T]:
    for item in iterable:
        if predicate(item):
            return item


def let_or_default(variable: bool, block: Callable[[], B], default: B) -> B:
    if variable:
        return block()
    return default


def let(variable: bool, block: Callable[[], B]) -> Optional[B]:
    if variable:
        return block()
