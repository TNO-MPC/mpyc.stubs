"""
Updated version of the MPyC Coroutine code file
A few alterations have been made to ensure that type hinting can be applied properly
"""

from __future__ import annotations

import sys
from typing import Any, Callable, Coroutine, TypeVar, no_type_check

import mpyc.runtime  # noqa # required, otherwise asyncoro.runtime might be None (set by mpyc.runtime upon module loading) and errors arise
from mpyc import asyncoro as mpyc_asyncoro
from mpyc.sectypes import SecureObject

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

SecureElement = TypeVar("SecureElement", bound=SecureObject)
T = TypeVar("T")
P = ParamSpec("P")


def mpc_coro_ignore(
    func: Callable[P, Coroutine[Any, None, SecureElement]]
) -> Callable[P, SecureElement]:
    """
    A wrapper for an MPC coroutine that ensures that the behaviour of the code is unaffected by
    the type annotations.

    :param func: The async function to be wrapped
    :return: A placeholder for which a result will automatically be set when the coroutine has
        finished running
    """
    return mpc_coro(func, apply_program_counter_wrapper=False, ignore_type_hints=True)


def mpc_coro(  # noqa: C901
    func: Callable[P, Coroutine[Any, None, SecureElement]],
    apply_program_counter_wrapper: bool = True,
    ignore_type_hints: bool = False,
) -> Callable[P, SecureElement]:
    """Decorator turning coroutine func into an MPyC coroutine.
    An MPyC coroutine is evaluated asynchronously, returning empty placeholders.
    The type of the placeholders is defined either by a return annotation
    of the form "-> expression" or by the first await expression in func.
    Return annotations can only be used for static types.

    :param func: The async function to be wrapped
    :param apply_program_counter_wrapper: A boolean value indicating whether a program counter
        wrapper should be applied
    :param ignore_type_hints: A boolean indicating whether type annotations should be used by the
        code to deduce the type of the placeholder
    :return: A placeholder for which a result will automatically be set when the coroutine has
        finished running
    """

    if ignore_type_hints:
        func = no_type_check(func)
    return mpyc_asyncoro.mpc_coro(func, pc=apply_program_counter_wrapper)


def returnType(  # type: ignore # This is redefinition of an mpyc method, so even though the name is
    # not camel case, we chose to keep it
    # pylint: disable=C0103,W9016,W9012 # Type annotations in overloaded methods
    return_type,
    *dimensions,
    wrap: bool = True,
):
    r"""
    Define return type for MPyC coroutines and expose it to send calls in an outer method.

    This function just delegates the call to the original definition of `returnType` in
    `mpyc.asyncoro`. Unfortunately, the type annotations are lost though in
    `mpc.returnType` due to the use of `staticmethod` which does not preserve overloads
    (mypy, v1.8.0). Alternatively, users could call `mpyc.asyncoro.returnType` directly but this
    seems counterintuitive and is hard to figure out. By exposing the method in
    `tno.mpc.mpyc.stubs` it is clearer that the standard mpc.returnType approach may not yield the
    expected results and we can provide this explanation.

    :param return_type: The class type of the object(s) to be returned
    :param \*dimensions: Arguments that describe the dimensions of the nested list to be returned.
        If no dimensions are provided, a single placeholder is returned. If one or more dimension
        is provided, it returns a nested list containing objects. The nesting is done according to
        the dimensions provided.
    :param wrap: If True, wrap the result into an Awaitable object.
    :return: A placeholder or nested list of placeholders (wrapped in an awaitable object) to
        expose the placeholder to an outer wrapper/coroutine.
    """
    return mpyc_asyncoro.returnType(return_type, *dimensions, wrap=wrap)
