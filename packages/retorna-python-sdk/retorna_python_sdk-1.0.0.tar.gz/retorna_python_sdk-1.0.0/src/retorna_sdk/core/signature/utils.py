import json
import time
from typing import Any, Dict


def stringify_query(params: Dict[str, Any]) -> str:
    """Converts query parameters into a sorted query string."""
    ordered = sorted((k, v) for k, v in params.items() if v is not None)
    return "&".join(f"{k}={v}" for k, v in ordered)


def generate_nonce() -> str:
    """Returns timestamp-based nonce."""
    return str(int(time.time() * 1000))


def minify_json(data: Dict[str, Any]) -> str:
    """Serializes the data into a compact JSON string."""
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
