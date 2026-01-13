"""Export generated mock data."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List


def export_to_json(data: Dict[str, List[dict]], output_dir: str) -> None:
    """Export each model records into separate JSON files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for model_name, records in data.items():
        file_path = output_path / f"{model_name}.json"

        with file_path.open("w", encoding="utf-8") as file_handle:
            json.dump(records, file_handle, indent=2, ensure_ascii=False, default=_json_default)

        print(f"Created {file_path} ({len(records)} records)")


def export_combined(data: Dict[str, List[dict]], output_file: str) -> None:
    """Export all model records into a single JSON file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, indent=2, ensure_ascii=False, default=_json_default)

    print(f"Created {output_path} ({sum(len(v) for v in data.values())} records)")


def _json_default(value: object) -> str:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)
