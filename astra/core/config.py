import json
import os

CONFIG_PATH = os.path.expanduser("~/.astra/config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}

    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f) or {}
    except (json.JSONDecodeError, OSError):
        return {}


def update_config(data):
    config = load_config()
    config.update(data)
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    return config
