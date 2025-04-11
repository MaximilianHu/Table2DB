Table2DB
=====

A small solo utility that loads tabular files (CSV/TSV) into a local SQLite database with basic schema inference. Good for quick data poking without setting up a full DB import pipeline.

Features
- Infer column types from sample rows
- Create or append to a SQLite table
- Handle CSV and TSV with configurable delimiter
- Simple CLI: point at a file, pick a table, done

Status
- Work in progress. Personal side project done in small evening/weekend chunks.

Quick sketch
- `table2db load data.csv --table sales --db app.db`
- `table2db load data.tsv --table notes --db app.db --delimiter '\t'`

