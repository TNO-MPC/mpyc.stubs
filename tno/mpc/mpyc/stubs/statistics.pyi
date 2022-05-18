from typing import Iterable, Sequence, TypeVar, Union

from mpyc.sectypes import SecureFixedPoint, SecureObject

SecureObjectType = TypeVar("SecureObjectType", bound=SecureObject)

def mean(
    data: Union[Iterable[SecureObjectType], Sequence[SecureObjectType]]
) -> SecureObjectType: ...
def median(
    data: Union[Iterable[SecureObjectType], Sequence[SecureObjectType]]
) -> SecureObjectType: ...
def stdev(
    data: Union[Iterable[SecureObjectType], Sequence[SecureObjectType]],
    xbar: bool = ...,
) -> SecureObjectType: ...
def _fsqrt(a: SecureFixedPoint) -> SecureFixedPoint: ...
