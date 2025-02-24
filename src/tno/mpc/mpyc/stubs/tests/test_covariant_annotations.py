"""
Tests for covariant type annotations (mypy) while making sure that mypy can actually handle these inputs.
"""

from __future__ import annotations

from functools import partial

import pytest
from mpyc.finfields import PrimeFieldElement
from mpyc.runtime import mpc
from mpyc.sectypes import SecureInteger


def field_to_stype(fld: PrimeFieldElement, stype: type[SecureInteger]) -> SecureInteger:
    """
    Convert a PrimeFieldElement to a SecureInteger.

    :param fld: Field element.
    :param stype: Type that needs to be instantiated.
    :return: Secure integer from prime field element.
    """
    return stype(fld.value)


@pytest.mark.asyncio
async def covariant_annotations() -> None:
    """
    Validate that covariant types can be passed as input arguments.

    We input Tuples just to be sure that this is not an issue (as expected when Sequence is the
    type annotation).

    We await actual outputs to make sure that the code is ran and pytest can detect issues.
    mpc.output actually requires list instances.
    """
    async with mpc:
        secint = mpc.SecInt()
        secint_elem = secint(1)
        secint_seq = (secint_elem,)
        secint_seq_shared = tuple(mpc.input([secint_elem], senders=0))

        field_to_secint = partial(field_to_stype, stype=secint)

        # mpc.from_bits
        await mpc.output(mpc.from_bits(secint_seq_shared))

        # mpc.gather
        await mpc.output(field_to_secint((await mpc.gather(secint_seq))[0]))
        await mpc.output(field_to_secint((await mpc.gather((secint_seq,)))[0][0]))
        await mpc.output(field_to_secint((await mpc.gather(((secint_seq,),)))[0][0][0]))
        await mpc.output(
            field_to_secint((await mpc.gather(secint_seq, secint_seq))[0][0])
        )
        await mpc.output(
            field_to_secint(
                (await mpc.gather(secint_seq, secint_seq, secint_seq))[0][0]
            )
        )

        # mpc.in_prod
        await mpc.output(mpc.in_prod(secint_seq_shared, secint_seq_shared))

        # mpc.matrix_prod
        await mpc.output(mpc.matrix_prod((secint_seq,), (secint_seq,))[0][0])

        # mpc.all
        await mpc.output(mpc.all(secint_seq))


def test_covariant_annotations() -> None:
    """
    Validate that covariant types can be passed as input arguments.
    """
    mpc.run(covariant_annotations())
