"""Pre-join star-schema CSVs into a single flat CSV for teaching join-less workbooks
that show students the 'after' state. Pairs with a teaching script that has them
reproduce the join live in Tableau.

Usage:
  python3 prejoin.py <output.csv> <left.csv> <right.csv:left_key=right_key> [more right files...]

Example:
  python3 prejoin.py joined.csv battles.csv venue.csv:venue_id=venue_id
  python3 prejoin.py joined.csv battle_participant.csv pokemon.csv:pokemonid=pokedex_number trainer.csv:trainer_id=trainer_id
"""
from __future__ import annotations
import sys
import pandas as pd
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 4:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    out = Path(sys.argv[1])
    left_path = Path(sys.argv[2])
    df = pd.read_csv(left_path)
    left_stem = left_path.stem
    for spec in sys.argv[3:]:
        path_part, keys = spec.split(":")
        left_key, right_key = keys.split("=")
        right_path = Path(path_part)
        right = pd.read_csv(right_path)
        right_stem = right_path.stem
        # Prefix right columns (except the join key) to avoid collisions
        right = right.rename(columns={c: f"{right_stem}_{c}" for c in right.columns if c != right_key})
        df = df.merge(right, how="left", left_on=left_key, right_on=right_key)
        if left_key != right_key and right_key in df.columns:
            df = df.drop(columns=[right_key])
    df.to_csv(out, index=False)
    print(f"wrote {out}: {len(df)} rows, {len(df.columns)} columns")
    print("columns:", list(df.columns))


if __name__ == "__main__":
    main()
