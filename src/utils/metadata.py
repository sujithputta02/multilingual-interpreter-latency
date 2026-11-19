"""Metadata and reproducibility tracking utilities."""
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


def get_environment_info() -> Dict[str, Any]:
    """Captures runtime environment details for reproducibility (PRD Section 16.3)."""
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Saves dictionary to JSON with formatting."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: str) -> Optional[Dict[str, Any]]:
    """Loads dictionary from JSON if it exists."""
    path = Path(filepath)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
