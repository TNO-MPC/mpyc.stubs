from typing import Any, Callable, ClassVar, List, Optional, Tuple, Type, TypeVar, Union

FieldTypePlaceholder = Any
T = TypeVar("T", bound="SecureObject")

runtime = None

class SecureObject:
    __slots__ = "share"
    def __init__(self, value: Optional[Any] = ...) -> None: ...

class SecureNumber(SecureObject):
    __slots__ = ()

    bit_length: ClassVar[Optional[int]] = ...
    def __neg__(self: T) -> T: ...
    def __pow__(self: T, other: int) -> T: ...
    def __pos__(self: T) -> T: ...
    def __abs__(self: T) -> T: ...
    def __add__(self: T, other: Union[T, float]) -> T: ...
    def __radd__(self: T, other: Union[T, float]) -> T: ...
    def __sub__(self: T, other: Union[T, float]) -> T: ...
    def __rsub__(self: T, other: Union[T, float]) -> T: ...
    def __mul__(self: T, other: Union[T, float]) -> T: ...
    def __rmul__(self: T, other: Union[T, float]) -> T: ...
    def __truediv__(self: T, other: Union[T, float]) -> T: ...
    def __rtruediv__(self: T, other: Union[T, float]) -> T: ...
    def __mod__(self: T, other: Union[T, int]) -> T: ...
    def __rmod__(self: T, other: Union[T, int]) -> T: ...
    def __floordiv__(self: T, other: int) -> T: ...
    def __rfloordiv__(self: T, other: int) -> T: ...
    def __divmod__(self: T, other: int) -> Tuple[T, T]: ...
    def __rdivmod__(self: T, other: int) -> Tuple[T, T]: ...
    def __lshift__(self: T, other: int) -> T: ...
    def __rlshift__(self: T, other: int) -> T: ...
    def __rshift__(self: T, other: int) -> T: ...
    def __rrshift__(self: T, other: int) -> T: ...
    def __and__(self: T, other: Union[int, T]) -> T: ...
    def __rand__(self: T, other: Union[int, T]) -> T: ...
    def __xor__(self: T, other: Union[int, T]) -> T: ...
    def __rxor__(self: T, other: Union[int, T]) -> T: ...
    def __invert__(self: T) -> T: ...
    def __or__(self: T, other: Union[int, T]) -> T: ...
    def __ror__(self: T, other: Union[int, T]) -> T: ...
    def __lt__(self: T, other: Union[float, T]) -> T: ...
    def __le__(self: T, other: Union[float, T]) -> T: ...
    def __eq__(self: T, other: Union[float, T]) -> T: ...  # type: ignore[override]
    def __ge__(self: T, other: Union[float, T]) -> T: ...
    def __gt__(self: T, other: Union[float, T]) -> T: ...
    def __ne__(self: T, other: Union[float, T]) -> T: ...  # type: ignore[override]

class SecureFiniteField(SecureNumber):
    __slots__ = ()

    frac_length: ClassVar[Optional[int]] = ...
    field: FieldTypePlaceholder = ...

    _output_conversion: ClassVar[
        Optional[Union[type, Callable[[Union[int, float]], Union[int, float]]]]
    ] = ...
    def __init__(
        self, value: Optional[Union[int, FieldTypePlaceholder]] = ...
    ) -> None: ...

class SecureInteger(SecureNumber):
    __slots__ = ()

    frac_length: ClassVar[int] = ...
    field: FieldTypePlaceholder = ...

    _output_conversion: ClassVar[Callable[[int], int]] = ...
    def __init__(
        self, value: Optional[Union[int, FieldTypePlaceholder]] = ...
    ) -> None: ...

class SecureFixedPoint(SecureNumber):
    """Base class for secure (secret-shared) fixed-point numbers."""

    __slots__ = "integral"

    frac_length: ClassVar[int] = ...
    field: FieldTypePlaceholder = ...
    @classmethod
    def _output_conversion(cls, a: Union[int, float]) -> float: ...
    def __init__(
        self,
        value: Optional[Union[int, float, FieldTypePlaceholder]] = ...,
        integral: Optional[bool] = ...,
    ) -> None:
        self.integral: bool = ...

def SecFld(
    order: Optional[int] = ...,
    modulus: Optional[Union[int, str, Any]] = ...,
    char: Optional[int] = ...,
    ext_deg: Optional[int] = ...,
    min_order: Optional[int] = ...,
    signed: bool = ...,
) -> Type[SecureFiniteField]: ...
def SecInt(
    l: Optional[int] = ..., p: Optional[int] = ..., n: int = ...
) -> Type[SecureInteger]: ...
def SecFxp(
    l: Optional[int] = ...,
    f: Optional[int] = ...,
    p: Optional[int] = ...,
    n: int = ...,
) -> Type[SecureFixedPoint]: ...

class SecureFloat(SecureNumber):
    __slots__ = ()

    significand_type: Optional[SecureObject] = ...
    exponent_type: Optional[SecureObject] = ...
    def __init__(self, value: Optional[Union[int, float]] = ...) -> None: ...
    @classmethod
    def _input(
        cls, x: List[SecureFloat], senders: List[int]
    ) -> List[List[SecureFloat]]: ...

def SecFlt(
    l: Optional[int] = ..., s: Optional[int] = ..., e: Optional[int] = None
) -> SecureFloat: ...
