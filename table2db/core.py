from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass
class Column:
    name: str
    decl: str


def _infer_type(values: Iterable[str]) -> str:
    is_int, is_float = True, True
    for v in values:
        s = v.strip()
        if s == "":
            continue
        if is_int:
            try:
                int(s)
            except ValueError:
                is_int = False
        if is_float:
            try:
                float(s)
            except ValueError:
                is_float = False
    if is_int:
        return "INTEGER"
    if is_float:
        return "REAL"
    return "TEXT"


def _sanitize(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)
    if cleaned and cleaned[0].isdigit():
        cleaned = f"c_{cleaned}"
    return cleaned or "col"


def _read_rows(path: Path, delimiter: str) -> Iterable[List[str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            yield [c if c is not None else "" for c in row]


def _create_table(conn: sqlite3.Connection, table: str, columns: Sequence[Column], replace: bool) -> None:
    cur = conn.cursor()
    qtable = f'"{table}"'
    if replace:
        cur.execute(f"DROP TABLE IF EXISTS {qtable}")
    colspec = ", ".join(f'"{c.name}" {c.decl}' for c in columns)
    cur.execute(f"CREATE TABLE IF NOT EXISTS {qtable} ({colspec})")
    conn.commit()


def load_table(conn: sqlite3.Connection, file: Path, table: str, *, delimiter: str = ",", sample_rows: int = 200, append: bool = False) -> None:
    rows = _read_rows(Path(file), delimiter)
    it = iter(rows)
    header = next(it)
    names = [_sanitize(h or f"col{i}") for i, h in enumerate(header)]

    sample: List[List[str]] = []
    for i, row in enumerate(it):
        sample.append(row)
        if i + 1 >= sample_rows:
            break

    transposed = list(map(list, zip(*sample))) if sample else [[] for _ in names]
    decls = [_infer_type(col_vals) for col_vals in transposed]
    columns = [Column(n, d) for n, d in zip(names, decls)]

    _create_table(conn, table, columns, replace=not append)

    # Insert header + all rows (including beyond the sample)
    placeholders = ",".join(["?"] * len(names))
    qtable = f'"{table}"'
    cur = conn.cursor()

    # Insert sampled rows first
    if sample:
        cur.executemany(f"INSERT INTO {qtable} VALUES ({placeholders})", sample)

    # Continue streaming remaining rows
    for row in it:
        cur.execute(f"INSERT INTO {qtable} VALUES ({placeholders})", row)

    conn.commit()

