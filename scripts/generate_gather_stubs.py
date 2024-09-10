"""
This script generates type hints for the mpc.gather function for a given number of arguments.
"""

from __future__ import annotations

from itertools import product

GATHER_TEMPLATE = (
    "    @overload\n    def gather(\n        self,\n{typing_in}\n    ) -> Awaitable"
    "[{typing_out}]: ...\n"
)

IN_TEMPLATE = "    obj_{number}: {in_type},"

PARAMETER_NRS = [1, 2, 3, 4]

intype_outtype_mapping = {
    "SecureObject": "PrimeFieldElement",
    "Sequence[SecureObject]": "list[PrimeFieldElement]",
    "Sequence[Sequence[SecureObject]]": "list[list[PrimeFieldElement]]",
    "Sequence[Sequence[Sequence[SecureObject]]]": "list[list[list[PrimeFieldElement]]]",
    "PrimeFieldElement": "PrimeFieldElement",
    "Sequence[PrimeFieldElement]": "list[PrimeFieldElement]",
    "Sequence[Sequence[PrimeFieldElement]]": "list[list[PrimeFieldElement]]",
    "Sequence[Sequence[Sequence[PrimeFieldElement]]]": "list[list[list[PrimeFieldElement]]]",
}


def get_arg_types_tuples(nr_args: int) -> list[tuple[str, ...]]:
    """
    Return a list denoting the Cartesian product of the typing_options keys for a certain number
    of arguments.

    :param nr_args: The number of arguments.
    :return: The list containing the Cartesian product.
    """
    arg_type = tuple(intype_outtype_mapping.keys())
    return list(product(arg_type, repeat=nr_args))


def tuple_to_annotated_function(tup: tuple[str, ...]) -> str:
    """
    Turn a tuple of argument types, represented by strings, into a string representing the
    overloaded typed mpc.gather
    method.

    :param tup: Tuple of argument types that represent the types of the arguments as input.
    :return: The overload mpc.gather code according to the provided arguments.
    """
    in_section = "\n    ".join(
        [
            IN_TEMPLATE.format(number=i + 1, in_type=in_type)
            for i, in_type in enumerate(tup)
        ]
    )
    out_section = ", ".join([intype_outtype_mapping[in_type] for in_type in tup])
    if len(tup) > 1:
        out_section = f"tuple[{out_section}]"
    return GATHER_TEMPLATE.format(typing_in=in_section, typing_out=out_section)


def generate_all_function_annotations(nr_args_list: list[int]) -> list[str]:
    """
    Generate all possible combinations of input types for the arguments to mpc.gather for a
    provided list of argument
    numbers and turn them into overloaded mpc.gather code.

    :param nr_args_list: List containing the number of arguments that should be considered for
        the typing code.
    :return: A list of strings denoting the various overloaded mpc.gather code resulting from the
        input.
    """
    return [
        tuple_to_annotated_function(tup)
        for tup in sum((get_arg_types_tuples(i) for i in nr_args_list), start=[])
    ]


def parameter_nrs_to_string(parameter_nrs: list[int]) -> str:
    """
    Turn a list of numbers to a textual enumeration.

    :param parameter_nrs: The numbers to be enumerated.
    :return: The final text.
    """
    if len(parameter_nrs) == 1:
        return f"{parameter_nrs[0]}"
    first_part = ", ".join(str(_) for _ in parameter_nrs[:-1])
    last_part = f" and {parameter_nrs[-1]}"
    return first_part + last_part


with open("gather_stubs.pyi", "w", encoding="utf8") as write_file:
    region_start = (
        f""
        f"    # region Extensive Gather Types "
        f"(for number of parameters {parameter_nrs_to_string(PARAMETER_NRS)} and "
        f"nesting depth {len(intype_outtype_mapping) - 1})\n"
        f"    # The type hints in this region have been automatically "
        f"generated using the `generate_gather_stubs.py` script\n\n"
    )
    REGION_END = "    # endregion"

    write_file.write(region_start)
    for function_annotations in generate_all_function_annotations(PARAMETER_NRS):
        write_file.write(function_annotations)
    write_file.write(REGION_END)
