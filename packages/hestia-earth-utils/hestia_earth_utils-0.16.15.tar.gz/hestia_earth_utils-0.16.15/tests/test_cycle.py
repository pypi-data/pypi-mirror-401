import os
import json
import pytest

from tests.utils import fixtures_path
from hestia_earth.utils.cycle import get_cycle_emissions_calculation_status

fixtures_folder = os.path.join(fixtures_path, "blank_node", "calculation_status")
_folders = [
    d
    for d in os.listdir(fixtures_folder)
    if os.path.isdir(os.path.join(fixtures_folder, d))
]


@pytest.mark.parametrize("folder", _folders)
def test_get_cycle_emissions_calculation_status(folder: str):
    with open(
        os.path.join(fixtures_folder, folder, "node.jsonld"), encoding="utf-8"
    ) as f:
        cycle = json.load(f)

    with open(
        os.path.join(
            fixtures_folder, folder, "emissions-emission-with-missing-inputs.json"
        ),
        encoding="utf-8",
    ) as f:
        expected = json.load(f)

    result = get_cycle_emissions_calculation_status(cycle)
    print(json.dumps(result, indent=2))
    assert result == expected
