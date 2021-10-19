from asyncio import Task
from typing import (
    Callable,
    Coroutine,
    Generator,
    Generic,
    List,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

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
    pc: bool = ...,
) -> Callable[..., InnerType]: ...
def mpc_coro_ignore(
    func: Callable[..., Coroutine[InnerType, None, InnerType]]
) -> Callable[..., InnerType]: ...

SomeType = TypeVar("SomeType")

class YieldAwaitable(Generic[SomeType]):
    def __init__(self, value: SomeType) -> None: ...
    def __await__(self) -> Generator[SomeType, None, None]: ...

@overload
def returnType(
    return_type: Type[InnerType],
    *dimensions: int,
) -> YieldAwaitable[Union[InnerType, List[InnerType], List[List[InnerType]]]]: ...
@overload
def returnType(
    return_type: Tuple[Type[SecureObject], bool],
    *dimensions: int,
) -> YieldAwaitable[
    Union[SecureFixedPoint, List[SecureFixedPoint], List[List[SecureFixedPoint]]]
]: ...
@overload
def returnType_no_wrap(
    return_type: Type[None],
    *dimensions: int,
) -> None: ...
@overload
def returnType_no_wrap(
    return_type: Type[InnerType],
    *dimensions: int,
) -> Union[InnerType, List[InnerType], List[List[InnerType]]]: ...
@overload
def returnType_no_wrap(
    return_type: Tuple[Type[SecureObject], bool],
    *dimensions: int,
) -> Union[SecureFixedPoint, List[SecureFixedPoint], List[List[SecureFixedPoint]]]: ...
