import json
from pathlib import Path
from typing import Any


def get_json(file_path: str | Path) -> dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
