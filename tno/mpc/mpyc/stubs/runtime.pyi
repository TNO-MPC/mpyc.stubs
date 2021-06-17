from argparse import Namespace
from types import TracebackType
from typing import (
    Any,
    Awaitable,
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

from mpyc.sectypes import SecureObject

TypePlaceholder = TypeVar("TypePlaceholder")
SecureObjectType = TypeVar("SecureObjectType", bound=SecureObject)

class Runtime:
    def __init__(self, pid: int, parties: Iterable[int], options: Namespace) -> None:
        self.pid = pid
        self.parties = tuple(parties)
        self.options = options
        self.threshold: int = options.threshold
    coroutine: staticmethod
    returnType: staticmethod
    SecFld: staticmethod
    SecInt: staticmethod
    SecFxp: staticmethod

    # Some of the functions below are actually async functions. However, MPyC
    # does not return Awaitables from these functions but rather SecureObjects
    # with an Awaitable `value` field. This causes issues with type hinting.
    # It seems that this workaround allows MyPy to work as intended.
    async def barrier(self, name: Optional[str] = None) -> None: ...
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
        senders: Optional[Sequence[int]] = None,
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
        senders: Optional[Sequence[int]] = None,
    ) -> List[List[SecureObjectType]]: ...
    def _randoms(
        self, sftype: Type[SecureObjectType], n: int, bound: Optional[int] = ...
    ) -> List[SecureObjectType]: ...
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
    ) -> Union[int, float]: ...
    @overload
    async def output(
        self,
        x: List[SecureObjectType],
        receivers: Optional[Union[Sequence[int], int]] = ...,
        threshold: Optional[int] = ...,
        raw: bool = ...,
    ) -> List[Union[int, float]]: ...
    @overload
    def convert(
        self, x: Sequence[SecureObjectType], ttype: Type[TypePlaceholder]
    ) -> List[TypePlaceholder]: ...
    @overload
    def convert(
        self, x: SecureObjectType, ttype: Type[TypePlaceholder]
    ) -> TypePlaceholder: ...
    def gather(self, *obj: object) -> Any: ...
    def div(
        self,
        a: Union[SecureObjectType, int, float],
        b: Union[SecureObjectType, int, float],
    ) -> SecureObjectType: ...
    def sum(
        self, x: Iterable[SecureObjectType], start: int = 0
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
        a: Union[int, float, SecureObjectType],
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
    def __init__(
        self, pid: int, host: Optional[str] = None, port: Optional[str] = None
    ):
        """Initialize a party with given party identity pid."""
        self.pid = pid
        self.host = host
        self.port = port

mpc: Runtime
