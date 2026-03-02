# Project 2 — User Registry CLI (PostgreSQL)

CLI application for managing users (CRUD + search) using PostgreSQL.

This project is a continuation of the JSON-based version (Project 1.6),
now refactored to use a real relational database and a repository layer.

---

## Features

- PostgreSQL storage (no JSON)
- Repository pattern (DB layer separated from CLI)
- Parameterized SQL queries (SQL injection safe)
- Error mapping (NotFound, UniqueViolation, RepoError)
- Full CRUD support
- Case-insensitive search (ILIKE)

---

## Requirements

- Python 3.10+
- PostgreSQL 13+
- psycopg v3

---

## Install dependencies

```bash
pip install "psycopg[binary]"


  Database Setup
## Create database
createdb user_registry

Or via psql:

psql -U postgres
CREATE DATABASE user_registry;
## Apply schema
psql -U stepan -d user_registry -h localhost -f schema.sql

This creates:
users table
Primary key
Unique constraint on phone
Indexes for search optimization

DSN Example
Repository expects a DSN string:
host=localhost port=5432 dbname=user_registry user=stepan password=YOUR_PASSWORD
Replace YOUR_PASSWORD with your actual password.

## Project Structure
project_2_user_registry_pg/
├── repo.py
├── schema.sql
├── db_test.py
├── user_registry.py   (CLI — in progress)
├── README.md
└── .gitignore

## Running (Temporary Test)
Until CLI is fully implemented:
python3 db_test.py

## Supported CLI Commands (Planned):
help
add
list
get <id>
delete <id>
update <id>
search <text>
exit

## Architecture
The application is divided into layers:
Repository Layer (repo.py)
Responsible for:
Database connection
SQL queries
Error translation
Returning structured data (dict rows)

## CLI Layer (user_registry.py)
Responsible for:
Command parsing
Input validation
User-friendly output
Handling repository exceptions
The CLI layer does not contain SQL.

## Error Handling
Repository maps low-level database errors to domain-level exceptions:

NotFoundError
UniqueViolationError
RepoError

This prevents infrastructure details from leaking into CLI.

## Author

Stepan Salmin
Backend learning project (Python + PostgreSQL)
