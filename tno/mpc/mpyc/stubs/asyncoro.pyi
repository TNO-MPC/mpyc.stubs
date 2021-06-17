from asyncio import Task
from typing import Callable, Coroutine, List, Type, TypeVar, Union, overload

from mpyc.sectypes import SecureFixedPoint, SecureObject

InnerType = TypeVar("InnerType")
ReturnType = Union[InnerType, List[InnerType], List[List[InnerType]]]

def _ncopy(nested_list: InnerType) -> InnerType: ...
@overload
def _nested_list(
    rt: Type[SecureObject],
    n: int,
    dims: List[int],
) -> ReturnType[SecureObject]: ...
@overload
def _nested_list(
    rt: Type[None],
    n: int,
    dims: List[int],
) -> ReturnType[None]: ...
@overload
def _nested_list(
    rt: Callable[..., SecureFixedPoint],
    n: int,
    dims: List[int],
) -> ReturnType[SecureFixedPoint]: ...
def __reconcile(decl: InnerType, givn: InnerType) -> None: ...
def _reconcile(decl: InnerType, task: Task[InnerType]) -> None: ...
def mpc_coro(
    f: Callable[..., Coroutine[InnerType, None, InnerType]],
    pc: bool = True,
) -> Callable[..., InnerType]: ...
