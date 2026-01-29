from dataclasses import dataclass
from typing import Generic, TypeVar, Union

S = TypeVar('S')
@dataclass
class Some[S]:
    value: S

T = TypeVar('T')
@dataclass
class Ok[T]:
    value: T

E = TypeVar('E')
@dataclass(frozen=True)
class Err(Generic[E], Exception):
    value: E

Result = Union[Ok[T], Err[E]]
