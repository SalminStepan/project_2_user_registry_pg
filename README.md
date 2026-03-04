# Project 2 — User Registry CLI (PostgreSQL)

CLI application for managing users (CRUD + search) using PostgreSQL.

This project is a continuation of the JSON-based version (Project 1.6), now refactored to use a real relational database and a repository layer.

## Features
* PostgreSQL storage (no JSON)
* Repository pattern (DB layer separated from CLI)
* Parameterized SQL queries (SQL injection safe)
* Error mapping (NotFoundError, UniqueViolationError, RepoError)
* Full CRUD support
* Case-insensitive search (`ILIKE`)

## Requirements
* Python 3.10+
* PostgreSQL 13+
* psycopg v3

Install dependencies:
```bash
pip install "psycopg[binary]"
```

## Database Setup

### Create database
```bash
createdb user_registry
```
Or via psql:
```sql
psql -U postgres
CREATE DATABASE user_registry;
```
### Apply schema

```bash
psql -U stepan -d user_registry -h localhost -f schema.sql
```

This creates:
* `users` table
* primary key
* unique constraint on `phone`
* indexes for search optimization

## Configuration
The application reads PostgreSQL DSN from environment variable:
```
USER_REGISTRY_DSN
```
Example:
```bash
export USER_REGISTRY_DSN="host=localhost port=5432 dbname=user_registry user=stepan password=YOUR_PASSWORD"
```
Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Running the CLI
Before starting the CLI you must set the database DSN via environment variable.
Example:

```bash
export USER_REGISTRY_DSN="host=localhost port=5432 dbname=user_registry user=stepan password=YOUR_PASSWORD"
```

Then start the CLI:

```bash
python3 user_registry.py
```

Example session:

```
> list
1: Ivan | +77001234567 | Almaty

> add
Name: Sergei
Phone: +7777777777
City: New York

> search york
2: Sergei | +7777777777 | New York
```


## Supported CLI Commands
```
help
add
list
get <id>
delete <id>
update <id>
search <text>
exit
```
## Project Structure
```
project_2_user_registry_pg/
├── repo.py
├── schema.sql
├── db_test.py
├── user_registry.py
├── README.md
└── .gitignore
```

## Architecture
The application is divided into layers.

### Repository Layer (`repo.py`)
Responsible for:
* database connection
* SQL queries
* error translation
* returning structured data (`dict` rows)

### CLI Layer (`user_registry.py`)
Responsible for:
* command parsing
* input validation
* user-friendly output
* handling repository exceptions
The CLI layer does **not** contain SQL.

## Error Handling
Repository maps low-level database errors to domain-level exceptions:
* `NotFoundError`
* `UniqueViolationError`
* `RepoError`

This prevents infrastructure details from leaking into CLI.

## Author
Stepan Salmin
Backend learning project (Python + PostgreSQL)

