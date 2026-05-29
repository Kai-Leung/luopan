from __future__ import annotations

import json
from typing import Any


def dump_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def load_json(value: str) -> Any:
    return json.loads(value)


def load_json_field(value: str) -> Any:
    return load_json(value)
