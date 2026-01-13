import json
from pathlib import Path


def json_config(filepath: Path | str):
    with open(filepath, "rb") as f:
        conf = json.load(f)
    return conf
