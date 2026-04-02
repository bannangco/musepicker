#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema.validators import Draft202012Validator


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "schemas"
    schema_files = sorted(root.glob("*.schema.json"))
    if not schema_files:
        print(f"No schema files found in {root}")
        return 1

    failures: list[str] = []
    for schema_file in schema_files:
        try:
            with schema_file.open("r", encoding="utf-8") as handle:
                schema = json.load(handle)
            Draft202012Validator.check_schema(schema)
            print(f"[ok] {schema_file.name}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{schema_file.name}: {exc}")

    if failures:
        print("Schema validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("All JSON schemas are valid Draft 2020-12 schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
