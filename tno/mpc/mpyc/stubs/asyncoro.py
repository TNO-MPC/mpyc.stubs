"""
Updated version of the MPyC Coroutine code file
A few alterations have been made to ensure that type hinting can be applied properly
"""

import functools
import sys
from asyncio import Future, Task
from typing import (
    Any,
    Callable,
    Coroutine,
    Generator,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

from mpyc.asyncoro import (  # type: ignore # some classes or methods cannot be found because they; were defined as protected
    __reconcile,
    _ncopy,
    _nested_list,
    _ProgramCounterWrapper,
    _reconcile,
    _wrap_in_coro,
    runtime,
)
from mpyc.sectypes import SecureFixedPoint, SecureObject

InnerType = Optional[SecureObject]
# Note that in principle, higher recursion can occur, but lists with a recursion level of higher
# than 2 are very unlikely
ReturnType = Union[InnerType, List[InnerType], List[List[InnerType]]]

SecureElement = TypeVar("SecureElement")


def mpc_coro_ignore(
    func: Callable[..., Coroutine[SecureElement, None, SecureElement]]
) -> Callable[..., SecureElement]:
    """
    A wrapper for an MPC coroutine that ensures that the behaviour of the code is unaffected by
    the type annotations.

    :param func: The async function to be wrapped
    :return: A placeholder for which a result will automatically be set when the coroutine has
        finished running
    """
    return mpc_coro(func, apply_program_counter_wrapper=False, ignore_type_hints=True)


def mpc_coro(  # noqa: C901
    func: Callable[..., Coroutine[SecureElement, None, SecureElement]],
    apply_program_counter_wrapper: bool = True,
    ignore_type_hints: bool = False,
) -> Callable[..., SecureElement]:
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

    rettype = None if ignore_type_hints else get_type_hints(func).get("return")

    @functools.wraps(func)
    def typed_asyncoro(*args: Any, **kwargs: Any) -> SecureElement:
        """
        This is the function that is returned when the mpc_coro wrapper is applied to an
        async function. This function creates the async coroutine that was wrapped using the
        positional arguments and keyword arguments and assigns the coroutine to a Task. A place-
        holder of the correct type is returned by this function and the value of the placeholder is
        substituted for the actual result when the Task has finished running the coroutine.

        :param args: positional arguments for the async function being wrapped
        :param kwargs: keyword arguments for the async function being wrapped
        :return: A placeholder of the right return type
        :raise Exception: This occurs when either the coroutine does not call returnType or another
            exception is raised while trying to retrieve the right return type.
        """
        runtime._pc_level += 1
        coro = func(*args, **kwargs)
        placeholder: SecureElement
        if rettype:
            placeholder = returnType_no_wrap(rettype)
        else:
            try:
                # attempting to reach an await returnType(...) statement
                placeholder = coro.send(None)
            except StopIteration as exc:
                # the coroutine returned a value, no returnType encountered
                # the value is not the placeholder but the actual result
                runtime._pc_level -= 1
                return_value: SecureElement = exc.value
                return return_value

            except Exception:
                runtime._pc_level -= 1
                raise

        # if this should not be done asynchronously, we exhaust the generator until we get a result
        if runtime.options.no_async:
            while True:
                try:
                    coro.send(None)
                except StopIteration as exc:
                    runtime._pc_level -= 1
                    if placeholder is not None:
                        __reconcile(placeholder, exc.value)
                    return placeholder

                except Exception:
                    runtime._pc_level -= 1  # pylint: disable=W0212
                    raise

        # we start a new Task that runs the coroutine and instruct it to replace the placeholder
        # when the coroutine has finished
        if apply_program_counter_wrapper:
            coro = _wrap_in_coro(
                _ProgramCounterWrapper(runtime, coro)
            )  # pylint: disable=W0212
        # start the coroutine in a different task
        task = Task(coro, loop=runtime._loop)  # pylint: disable=W0212
        # enclosing MPyC coroutine call
        # noinspection PyUnresolvedReferences
        # the method is protected, but we do need it, so the inspection tools will throw an error
        task.f_back = sys._getframe(1)  # type: ignore # pylint: disable=W0212

        # make sure the placeholder is replaced after the coroutine is finished
        task.add_done_callback(lambda t: _reconcile(placeholder, t))
        placeholder_copy = _ncopy(placeholder)
        return placeholder_copy

    return typed_asyncoro


SomeType = TypeVar("SomeType")


class YieldAwaitable(
    Generic[SomeType]
):  # pylint: disable=R0903 # This is a redefinition of an mpyc method.
    # The error message claims there are too few public methods for this class
    """
    A class to be applied to values that need to be available to an outer function through the
    send method.
    """

    __slots__ = ["value"]

    def __init__(self, value: SomeType) -> None:
        self.value = value

    def __await__(self) -> Generator[SomeType, None, None]:
        """
        Trick to send the stored value to the outer MPyC coroutine wrapper when the
        Awaitable is awaited. The yield statement is caught by the outer wrapper by calling
        the send method of the coroutine it wraps around.

        :return: A generator yielding the stored value
        """
        yield self.value


def returnType(  # type: ignore # This is redefinition of an mpyc method, so even though the name is
    # not camel case, we chose to keep it
    # pylint: disable=C0103,W9016,W9012 # Type annotations in overloaded methods
    return_type,
    *dimensions,
):
    """
    Define return type for MPyC coroutines and expose it to send calls in an outer method.
    It is used in first await expression in an MPyC coroutine. The YieldAwaitable assures that a
    call to await returnType passes the return type to the outer mpc_coro wrapper.

    :param return_type: The Class type of the object(s) to be returned
    :param dimensions: arguments that describe the dimensions of the nested list to be returned. If
        no dimensions are provided, a single placeholder is returned. If one or more dimension is
        provided, it returns a nested list containing objects. The nesting is done according to the
        dimensions provided.
    :return: A placeholder or nested list of placeholders wrapped in a YieldAwaitable to expose the
        placeholder to an outer wrapper/coroutine.
    """
    return YieldAwaitable(returnType_no_wrap(return_type, *dimensions))


def returnType_no_wrap(  # type: ignore # This is redefinition of an mpyc method,
    # so even though the name is not camel case, we chose to keep it
    # pylint: disable=C0103,W9016,W9012 # Type annotations in overloaded methods
    return_type,
    *dimensions,
):
    """
    Define return type for MPyC coroutines.

    :param return_type: The Class type of the placeholder
    :param dimensions: arguments that describe the dimensions of the nested list to be returned.
        If no dimensions are provided, a single placeholder is returned. If one or more dimension
        is provided, it returns a nested list containing objects. The nesting is done according to the
        dimensions provided.
    :return: A placeholder or nested list of placeholders wrapped.
    """
    dimension_list = list(dimensions)
    if isinstance(return_type, type(None)):
        return None

    if isinstance(return_type, tuple):
        secure_type, integral = return_type
        if secure_type.frac_length:
            # we now know that the return_type is a class constructor for a class that is a
            # subclass of SecureFixedPoint
            def return_placeholder() -> SecureFixedPoint:
                """
                Quick workaround to allow a function that returns a placeholder
                to be saved in a variable

                :return: Secure fixed-point number
                """
                return secure_type(None, integral)  # type: ignore # we know that this must be a
                # SecureFixedPoint, so the constructor can be called with 2 parameters

            temp_return_type = return_placeholder
        else:
            temp_return_type = secure_type
    # NOTE: This part is ignored for type hinting
    elif issubclass(return_type, Future):
        # pylint: disable=W0212
        temp_return_type = lambda: return_type(loop=runtime._loop)  # type: ignore # This returns a
        # Future, but this is not understood by the inspection tools
        # pylint: enable=W0212
    else:
        temp_return_type = return_type

    if dimension_list:
        # create a nested list of placeholders
        return _nested_list(temp_return_type, dimension_list[0], dimension_list[1:])

    temp_return_type_no_none: Union[
        Type[SecureObject], Callable[..., SecureFixedPoint]
    ] = temp_return_type
    return temp_return_type_no_none()
