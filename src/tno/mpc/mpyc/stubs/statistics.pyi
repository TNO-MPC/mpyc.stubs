from __future__ import annotations

from typing import Iterable, Sequence, TypeVar

from mpyc.sectypes import SecureFixedPoint, SecureObject

SecureObjectType = TypeVar("SecureObjectType", bound=SecureObject)

def mean(
    data: Iterable[SecureObjectType] | Sequence[SecureObjectType],
) -> SecureObjectType: ...
def median(
    data: Iterable[SecureObjectType] | Sequence[SecureObjectType],
) -> SecureObjectType: ...
def stdev(
    data: Iterable[SecureObjectType] | Sequence[SecureObjectType],
    xbar: bool = ...,
) -> SecureObjectType: ...
def _fsqrt(a: SecureFixedPoint) -> SecureFixedPoint: ...
