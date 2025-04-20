import argparse
import sqlite3
from pathlib import Path
from .core import load_table
from .util import normalize_delimiter


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="table2db", description="Load CSV/TSV into SQLite")
    sub = p.add_subparsers(dest="cmd", required=True)

    lp = sub.add_parser("load", help="Load a tabular file into SQLite")
    lp.add_argument("file", type=Path, help="CSV or TSV file path")
    lp.add_argument("--db", required=True, help="SQLite database file path")
    lp.add_argument("--table", required=True, help="Target table name")
    lp.add_argument("--delimiter", default=",", help="Field delimiter, default ',' (use \t for TSV)")
    lp.add_argument("--sample", type=int, default=200, help="Rows to sample for type inference")
    lp.add_argument("--append", action="store_true", help="Append to existing table instead of replacing")
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    conn = sqlite3.connect(args.db)
    try:
        delim = normalize_delimiter(args.delimiter)
        load_table(conn, args.file, args.table, delimiter=delim, sample_rows=args.sample, append=args.append)
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
