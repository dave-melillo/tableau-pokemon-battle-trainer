"""Inspect a CSV and emit a column profile (name, inferred type, role hint, samples)."""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path
from collections import Counter


TABLEAU_TYPES = {"integer", "real", "string", "date", "datetime", "boolean"}


def infer_column_type(values: list[str]) -> str:
    samples = [v for v in values if v not in ("", None)]
    if not samples:
        return "string"
    int_ok = real_ok = date_ok = True
    for v in samples[:200]:
        if int_ok:
            try:
                int(v)
            except ValueError:
                int_ok = False
        if real_ok:
            try:
                float(v)
            except ValueError:
                real_ok = False
        if date_ok:
            if not (len(v) >= 8 and v[:4].isdigit() and ("-" in v or "/" in v)):
                date_ok = False
    if int_ok:
        return "integer"
    if real_ok:
        return "real"
    if date_ok:
        return "date"
    return "string"


def role_hint(name: str, dtype: str, distinct_ratio: float) -> str:
    """Guess dimension vs measure. Numeric IDs with low cardinality look like dimensions."""
    if dtype == "string":
        return "dimension"
    if dtype in ("date", "datetime"):
        return "dimension"
    if dtype in ("integer", "real"):
        if distinct_ratio < 0.05 or name.lower().endswith("_id") or name.lower() == "id":
            return "dimension"
        return "measure"
    return "dimension"


def inspect(csv_path: Path) -> dict:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    cols = []
    for i, name in enumerate(headers):
        values = [r[i] if i < len(r) else "" for r in rows]
        dtype = infer_column_type(values)
        distinct = len(set(values))
        ratio = distinct / max(len(values), 1)
        sample = [v for v in values[:5] if v]
        cols.append({
            "name": name,
            "datatype": dtype,
            "role": role_hint(name, dtype, ratio),
            "distinct_count": distinct,
            "sample": sample,
        })
    return {
        "file": str(csv_path),
        "row_count": len(rows),
        "columns": cols,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: inspect_data.py <csv-file>", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(inspect(Path(sys.argv[1])), indent=2))
