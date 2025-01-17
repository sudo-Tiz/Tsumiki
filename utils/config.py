import json
import os

from fabric.utils import get_relative_path

from utils.constants import DEFAULT_CONFIG


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
