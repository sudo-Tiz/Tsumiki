import json
import os

from fabric.utils import get_relative_path

from .constants import DEFAULT_CONFIG
from .functions import exclude_keys, merge_defaults, validate_widgets
from .widget_settings import BarConfig


# Function to read the configuration file
def read_config():
    config_file = get_relative_path("../config.json")
    if not os.path.exists(config_file):
        with open(config_file, "w") as destination_file:
            json.dump(DEFAULT_CONFIG, destination_file, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG

    with open(config_file) as file:
        # Load JSON data into a Python dictionary
        data = json.load(file)
    return data


def default_config() -> BarConfig:
    # Read the configuration from the JSON file
    parsed_data = read_config()

    validate_widgets(parsed_data, DEFAULT_CONFIG)

    for key in exclude_keys(DEFAULT_CONFIG, ["$schema"]):
        parsed_data[key] = merge_defaults(parsed_data.get(key, {}), DEFAULT_CONFIG[key])

    return parsed_data


widget_config = default_config()
