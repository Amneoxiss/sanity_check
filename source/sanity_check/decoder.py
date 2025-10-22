from typing import Dict, List, Union
import yaml

from .sanity import Sanity, SanityFailLevel


def create_sanity_from_data(data: Dict[str, Union[str, bool]]) -> Sanity:
        sanity_class = data.get("class")

        if not sanity_class:
            raise ValueError("Sanity 'class' is not defined.")

        module, _, callable_name = sanity_class.rpartition(".")
        try:
            sanity = getattr(module, callable_name)
        except (ModuleNotFoundError, AttributeError) as err:
            raise ValueError(f"Could not find Sanity '{sanity_class}'.")

        nice_name = data.get("nice_name")

        if not nice_name:
            raise ValueError("Sanity 'nice_name' is not defined.")

        if not isinstance(nice_name, str):
            raise TypeError(f"'nice_name' should be a string, not a '{type(nice_name)}'")

        fail_level = data.get("fail_level")

        if not fail_level:
            raise ValueError("Sanity 'fail_level' is not defined.")

        try:
            fail_level = SanityFailLevel[fail_level]
        except ValueError as err:
            raise ValueError("fail_level doesn't a valid value.") from err

        default_check = data.get("default_check")

        if not default_check:
            raise ValueError("default_check is not defined.")

        if not isinstance(default_check, bool):
            raise TypeError(f"'default_check' should be a bool, not a '{type(default_check)}'")

        sanity_obj = sanity(nice_name, fail_level, default_check)
        
        return sanity_obj


def decode_yaml(yaml_file_path) -> Dict[str, List[Sanity]]:
    with open(yaml_file_path, 'r') as read_file:
        data: dict = yaml.safe_load(read_file)

    section_to_sanity_map = {}

    for section, sanity_list in data.items():
        # TODO: Rework error handling.
        section_to_sanity_map[section] = [create_sanity_from_data(sanity_data) for sanity_data in sanity_list]

    return section_to_sanity_map
