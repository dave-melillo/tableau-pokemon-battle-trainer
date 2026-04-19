"""Convert a CSV into a Tableau .hyper extract using the official Hyper API.

The extract uses schema='Extract', table='Extract', matching what Tableau Desktop produces.
Column types are taken from the supplied `columns` list (same shape build_twbx.py uses).
"""
from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path

from tableauhyperapi import (
    HyperProcess,
    Connection,
    CreateMode,
    Telemetry,
    TableDefinition,
    TableName,
    SqlType,
    Nullability,
    Inserter,
)


_TYPE_MAP = {
    "integer": SqlType.big_int(),
    "real": SqlType.double(),
    "string": SqlType.text(),
    "date": SqlType.date(),
    "datetime": SqlType.timestamp(),
    "boolean": SqlType.bool(),
}


def _coerce(val: str, dtype: str):
    if val == "" or val is None:
        return None
    try:
        if dtype == "integer":
            return int(float(val))
        if dtype == "real":
            return float(val)
        if dtype == "boolean":
            return val.strip().lower() in ("1", "true", "t", "yes", "y")
        if dtype == "date":
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(val, fmt).date()
                except ValueError:
                    continue
            return None
        if dtype == "datetime":
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(val, fmt)
                except ValueError:
                    continue
            return None
        return val
    except (ValueError, TypeError):
        return None


def csv_to_hyper(csv_path: Path, hyper_path: Path, columns: list[dict]) -> None:
    """Write the CSV at csv_path into a .hyper extract at hyper_path.

    Only columns listed in `columns` are exported; CSV columns not in the list are skipped.
    """
    csv_path = Path(csv_path)
    hyper_path = Path(hyper_path)
    hyper_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        # index for each requested column
        col_indexes = []
        for c in columns:
            try:
                col_indexes.append((headers.index(c["name"]), c))
            except ValueError:
                raise ValueError(f"column {c['name']!r} not found in CSV headers: {headers}")
        rows = []
        for row in reader:
            row_out = []
            for idx, col in col_indexes:
                raw = row[idx] if idx < len(row) else ""
                row_out.append(_coerce(raw, col["datatype"]))
            rows.append(row_out)

    table_def = TableDefinition(
        table_name=TableName("Extract", "Extract"),
        columns=[
            TableDefinition.Column(c["name"], _TYPE_MAP.get(c["datatype"], SqlType.text()), Nullability.NULLABLE)
            for _, c in col_indexes
        ],
    )

    if hyper_path.exists():
        hyper_path.unlink()

    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(
            endpoint=hyper.endpoint,
            database=hyper_path,
            create_mode=CreateMode.CREATE_AND_REPLACE,
        ) as conn:
            conn.catalog.create_schema("Extract")
            conn.catalog.create_table(table_def)
            with Inserter(conn, table_def) as inserter:
                inserter.add_rows(rows)
                inserter.execute()
