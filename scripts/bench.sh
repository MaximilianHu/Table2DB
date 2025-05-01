#!/usr/bin/env bash
set -euo pipefail
db="${1:-bench.db}"
rm -f "$db"
python -m table2db.cli load examples/sales.csv --db "$db" --table sales
python - <<'PY'
import sqlite3,sys
conn=sqlite3.connect(sys.argv[1])
cur=conn.cursor()
print(cur.execute('select count(*) from sales').fetchone()[0])
PY
