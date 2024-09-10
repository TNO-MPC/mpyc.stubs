from __future__ import annotations

from typing import overload

from mpyc.finfields import PrimeFieldElement

@overload
def recombine(
    field: type[PrimeFieldElement],
    points: list[tuple[int, list[int]]],
    x_rs: int = 0,
) -> list[PrimeFieldElement]: ...
@overload
def recombine(
    field: type[PrimeFieldElement],
    points: list[tuple[int, list[int]]],
    x_rs: list[int],
) -> list[list[PrimeFieldElement]]: ...
