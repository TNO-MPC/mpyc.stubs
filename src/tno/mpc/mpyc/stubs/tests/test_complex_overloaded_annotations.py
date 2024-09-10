"""
Tests for type annotations (mypy) that have complex (conflicting) overloads.
"""

from __future__ import annotations

from mpyc.runtime import mpc
from mpyc.sectypes import SecureInteger

secnum = mpc.SecInt()
sec_list = list(map(secnum, range(4)))


# pylint: disable=missing-function-docstring
class TestOverloadsMax:
    """
    Validate the overloads of mpc.max.
    """

    def test_scalar_input_yield_scalar(self) -> None:
        result: SecureInteger = mpc.max(*sec_list)  # mypy check
        assert isinstance(result, secnum)

    def test_iter_input_yields_scalar(self) -> None:
        result: SecureInteger = mpc.max(sec_list)  # mypy check
        assert isinstance(result, secnum)

    def test_single_list_input_yields_scalar(self) -> None:
        result: SecureInteger = mpc.max(iter(sec_list))  # mypy check
        assert isinstance(result, secnum)

    def test_multiple_list_input_yields_list(self) -> None:
        result: list[SecureInteger] = mpc.max(sec_list, sec_list)  # mypy check
        assert isinstance(result, list)
