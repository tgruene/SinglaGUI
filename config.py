import json
import logging
import os.path


def load_config_files():
    config = {}
    _override(config, _load_config("etc/singlaui_config.json"))
    _override(config, _load_config(os.path.expanduser("~/.config/singlaui_config.json")))
    return config


def _load_config(path):
    try:
        with open(path) as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        logging.warning("Could not find config file " + path)
    except PermissionError:
        logging.error("Cannot read config file " + path)
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config file" + path)
    return {}


def _override(destination, source):
    for key in source.keys():
        destination[key] = source[key]
