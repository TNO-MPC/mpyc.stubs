from __future__ import annotations

import sys
from asyncio import Future, Task
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generator,
    Generic,
    List,
    Literal,
    TypeVar,
    Union,
    overload,
)

from mpyc.finfields import PrimeFieldElement
from mpyc.runtime import Runtime
from mpyc.sectypes import SecureObject

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

InnerT = TypeVar("InnerT")
ReturnType = Union[InnerT, List[InnerT], List[List[InnerT]]]
SomeT = TypeVar("SomeT")
AnotherT = TypeVar("AnotherT")
SecureObjectT = TypeVar("SecureObjectT", bound=SecureObject)
P = ParamSpec("P")

def _ncopy(nested_list: InnerT) -> InnerT: ...
@overload
def _nested_list(
    rt: type[SecureObjectT] | Callable[[], SecureObjectT],
    n: int,
    dims: list[int],
) -> ReturnType[SecureObjectT]: ...
@overload
def _nested_list(
    rt: type[None],
    n: int,
    dims: list[int],
) -> ReturnType[None]: ...
@overload
def __reconcile(
    decl: list[list[SecureObjectT | Future[SecureObjectT]]],
    givn: list[list[SecureObjectT | PrimeFieldElement]],
) -> None: ...
@overload
def __reconcile(
    decl: list[SecureObjectT | Future[SecureObjectT]],
    givn: list[SecureObjectT | PrimeFieldElement],
) -> None: ...
@overload
def __reconcile(
    decl: SecureObjectT | Future[SecureObjectT],
    givn: SecureObjectT | PrimeFieldElement,
) -> None: ...
@overload
def _reconcile(decl: None, task: Any) -> None: ...
@overload
def _reconcile(
    decl: list[list[SecureObjectT | Future[SecureObjectT]]],
    givn: Task[list[list[SecureObjectT | PrimeFieldElement]]],
) -> None: ...
@overload
def _reconcile(
    decl: list[SecureObjectT | Future[SecureObjectT]],
    givn: Task[list[SecureObjectT | PrimeFieldElement]],
) -> None: ...
@overload
def _reconcile(
    decl: SecureObjectT | Future[SecureObjectT],
    givn: Task[SecureObjectT | PrimeFieldElement],
) -> None: ...
def mpc_coro(
    f: Callable[P, Coroutine[Any, None, InnerT]],
    pc: bool = ...,
) -> Callable[P, InnerT]: ...
def mpc_coro_ignore(
    func: Callable[P, Coroutine[Any, None, InnerT]]
) -> Callable[P, InnerT]: ...

class _Awaitable(Generic[SomeT]):
    def __init__(self, value: SomeT) -> None: ...
    def __await__(self) -> Generator[SomeT]: ...

class _AwaitableFuture(Awaitable[SomeT]):
    def __init__(self, value: SomeT) -> None: ...
    def __await__(self) -> Generator[None, None, SomeT]: ...

class _ProgramCounterWrapper(Generic[SomeT, AnotherT]):
    def __init__(self, rt: Runtime, coro: Coroutine[SomeT, None, AnotherT]) -> None: ...

    rt: Runtime
    coro: Coroutine[SomeT, None, AnotherT]
    pc: list[int]

    def __await__(self) -> Generator[SomeT, None, AnotherT]: ...

async def _wrap_in_coro(awaitable: Awaitable[SomeT]) -> SomeT: ...
@overload
def returnType(
    return_type: type[InnerT],
    *dimensions: int,
    wrap: Literal[True] = ...,
) -> (
    _AwaitableFuture[InnerT]
    | _AwaitableFuture[list[InnerT]]
    | _AwaitableFuture[list[list[InnerT]]]
): ...
@overload
def returnType(
    return_type: type[InnerT],
    *dimensions: int,
    wrap: Literal[False],
) -> InnerT | list[InnerT] | list[list[InnerT]]: ...
@overload
def returnType(
    return_type: tuple[type[SecureObjectT], bool],
    *dimensions: int,
    wrap: Literal[True] = ...,
) -> (
    _AwaitableFuture[SecureObjectT]
    | _AwaitableFuture[list[SecureObjectT]]
    | _AwaitableFuture[list[list[SecureObjectT]]]
): ...
@overload
def returnType(
    return_type: tuple[type[SecureObjectT], bool],
    *dimensions: int,
    wrap: Literal[False],
) -> SecureObjectT | list[SecureObjectT] | list[list[SecureObjectT]]: ...
