from argparse import Namespace
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

import mpyc.sectypes as sectypes
from mpyc.sectypes import SecureObject

TypePlaceholder = TypeVar("TypePlaceholder")
SecureObjectType = TypeVar("SecureObjectType", bound=SecureObject)

class Runtime:
    def __init__(self, pid: int, parties: Iterable[Party], options: Namespace) -> None:
        self.pid = pid
        self.parties = tuple(parties)
        self.options = options
        self.threshold: int
    coroutine: staticmethod
    returnType: staticmethod
    SecFld: staticmethod = staticmethod(sectypes.SecFld)
    SecInt: staticmethod = staticmethod(sectypes.SecInt)
    SecFxp: staticmethod = staticmethod(sectypes.SecFxp)

    # Some of the functions below are actually async functions. However, MPyC
    # does not return Awaitables from these functions but rather SecureObjects
    # with an Awaitable `value` field. This causes issues with type hinting.
    # It seems that this workaround allows MyPy to work as intended.
    async def barrier(self, name: Optional[str] = ...) -> None: ...
    async def __aenter__(self) -> Awaitable[Runtime]: ...
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> Awaitable[Optional[bool]]: ...
    async def transfer(
        self,
        obj: Any,
        senders: Optional[Union[Sequence[int], int]] = ...,
        receivers: Optional[Union[Sequence[int], int]] = ...,
        sender_receivers: Optional[Union[Dict[int, int], Tuple[int, int]]] = ...,
    ) -> Any: ...
    @overload
    def input(
        self,
        x: SecureObjectType,
        senders: int,
    ) -> SecureObjectType: ...
    @overload
    def input(
        self,
        x: SecureObjectType,
        senders: Optional[Sequence[int]] = ...,
    ) -> List[SecureObjectType]: ...
    @overload
    def input(
        self,
        x: Sequence[SecureObjectType],
        senders: int,
    ) -> List[SecureObjectType]: ...
    @overload
    def input(
        self,
        x: Sequence[SecureObjectType],
        senders: Optional[Sequence[int]] = ...,
    ) -> List[List[SecureObjectType]]: ...
    def _randoms(
        self, sftype: Type[SecureObjectType], n: int, bound: Optional[int] = ...
    ) -> List[SecureObjectType]: ...
    def random_bits(
        self, sftype: Type[SecureObjectType], n: int, signed: bool = ...
    ) -> List[int]: ...
    @overload
    def matrix_prod(
        self,
        A: Sequence[Sequence[SecureObjectType]],
        B: Sequence[Sequence[float]],
        tr: bool = ...,
    ) -> List[List[SecureObjectType]]: ...
    @overload
    def matrix_prod(
        self,
        A: Sequence[Sequence[float]],
        B: Sequence[Sequence[SecureObjectType]],
        tr: bool = ...,
    ) -> List[List[SecureObjectType]]: ...
    @overload
    def matrix_prod(
        self,
        A: Sequence[Sequence[SecureObjectType]],
        B: Sequence[Sequence[SecureObjectType]],
        tr: bool = ...,
    ) -> List[List[SecureObjectType]]: ...
    async def shutdown(self) -> None: ...
    @overload
    async def output(
        self,
        x: SecureObjectType,
        receivers: Optional[Union[Sequence[int], int]] = ...,
        threshold: Optional[int] = ...,
        raw: bool = ...,
    ) -> float: ...
    @overload
    async def output(
        self,
        x: List[SecureObjectType],
        receivers: Optional[Union[Sequence[int], int]] = ...,
        threshold: Optional[int] = ...,
        raw: bool = ...,
    ) -> List[float]: ...
    @overload
    async def _reshare(
        self,
        x: SecureObjectType,
    ) -> SecureObjectType: ...
    @overload
    async def _reshare(
        self,
        x: List[SecureObjectType],
    ) -> List[SecureObjectType]: ...
    @overload
    def convert(
        self, x: Sequence[SecureObjectType], ttype: Type[TypePlaceholder]
    ) -> List[TypePlaceholder]: ...
    @overload
    def convert(
        self, x: SecureObjectType, ttype: Type[TypePlaceholder]
    ) -> TypePlaceholder: ...
    @overload
    def trunc(
        self, x: List[SecureObjectType], f: Optional[int] = ..., l: Optional[int] = ...
    ) -> List[SecureObjectType]: ...
    @overload
    def trunc(
        self, x: SecureObjectType, f: Optional[int] = ..., l: Optional[int] = ...
    ) -> SecureObjectType: ...
    async def is_zero_public(self, a: SecureObjectType) -> Awaitable[bool]: ...
    def sub(
        self, a: SecureObjectType, b: Union[SecureObjectType, float]
    ) -> SecureObjectType: ...
    def gather(self, *obj: object) -> Any: ...
    def lt(
        self, a: SecureObjectType, b: Union[SecureObjectType, float]
    ) -> SecureObjectType: ...
    def eq(
        self, a: SecureObjectType, b: Union[SecureObjectType, float]
    ) -> SecureObjectType: ...
    def ge(
        self, a: SecureObjectType, b: Union[SecureObjectType, float]
    ) -> SecureObjectType: ...
    def abs(self, a: SecureObjectType) -> SecureObjectType: ...
    def sgn(
        self, a: SecureObjectType, l: int = ..., LT: bool = ..., EQ: bool = ...
    ) -> SecureObjectType: ...
    def max(
        self, *x: Sequence[SecureObjectType], key: Optional[Callable[[Any], Any]] = ...
    ) -> SecureObjectType: ...
    def div(
        self,
        a: Union[SecureObjectType, float],
        b: Union[SecureObjectType, float],
    ) -> SecureObjectType: ...
    def sum(
        self, x: Iterable[SecureObjectType], start: int = ...
    ) -> SecureObjectType: ...
    def in_prod(
        self, x: Sequence[SecureObjectType], y: Sequence[SecureObjectType]
    ) -> SecureObjectType: ...
    def prod(
        self, x: Sequence[SecureObjectType], start: int = ...
    ) -> SecureObjectType: ...
    def vector_add(
        self, x: Sequence[SecureObjectType], y: Sequence[SecureObjectType]
    ) -> List[SecureObjectType]: ...
    def vector_sub(
        self, x: Sequence[SecureObjectType], y: Sequence[SecureObjectType]
    ) -> List[SecureObjectType]: ...
    def scalar_mul(
        self,
        a: Union[float, SecureObjectType],
        x: Sequence[SecureObjectType],
    ) -> List[SecureObjectType]: ...
    def schur_prod(
        self, x: Sequence[SecureObjectType], y: Sequence[SecureObjectType]
    ) -> List[SecureObjectType]: ...
    def run(
        self: Runtime, f: Coroutine[Any, None, TypePlaceholder]
    ) -> TypePlaceholder: ...
    async def start(self) -> None: ...

class Party:
    __slots__ = "pid", "host", "port", "protocol"
    def __init__(self, pid: int, host: Optional[str] = ..., port: Optional[int] = ...):
        """Initialize a party with given party identity pid."""
        self.pid = pid
        self.host = host
        self.port = port

mpc: Runtime
