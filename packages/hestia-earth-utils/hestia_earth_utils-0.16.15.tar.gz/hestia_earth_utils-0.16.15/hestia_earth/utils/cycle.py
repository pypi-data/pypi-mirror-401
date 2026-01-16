from hestia_earth.schema import TermTermType

from .tools import flatten
from .blank_node import get_blank_nodes_calculation_status


def _extend_missing_values(
    value: dict, all_values: set, key: str, must_have_key: bool = False
):
    included_values = set(flatten([v.get(key, []) for v in value.values()]))
    missing_values = all_values - included_values
    return (
        {"missing" + key.capitalize(): sorted(list(missing_values))}
        if all([missing_values, not must_have_key or included_values])
        else {}
    )


def get_cycle_emissions_calculation_status(cycle: dict):
    """
    Get calculation status for Cycle emissions included in the HESTIA system boundary.

    Parameters
    ----------
    cycle : dict
        The dictionary representing the Cycle.

    Returns
    -------
    dict
        A dictionary of `key:value` pairs representing each emission in the system boundary,
        and the resulting calculation as value, containing the recalculated `value`, `method` and `methodTier`.
        Note: if a calculation fails for an emission, the `value` is an empty dictionary.
    """
    status = get_blank_nodes_calculation_status(
        cycle, "emissions", TermTermType.EMISSION
    )
    input_ids = set([v.get("term", {}).get("@id") for v in cycle.get("inputs", [])])
    transformation_ids = set(
        [v.get("term", {}).get("@id") for v in cycle.get("transformations", [])]
    )
    return {
        k: v
        | (
            _extend_missing_values(v, input_ids, "inputs")
            if "InputsProduction" in k
            else {}
        )
        | (
            _extend_missing_values(
                v, transformation_ids, "transformations", must_have_key=True
            )
        )
        for k, v in status.items()
    }
