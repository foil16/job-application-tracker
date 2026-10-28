# Job Application Tracker

A REST API for tracking job applications: which companies you applied to, for what role, and where each application stands.

> **Status: in progress.** User registration and the database schema are done. JWT login and the applications endpoints are next.

## Tech stack

- **Python 3.14** with **FastAPI** and **Pydantic** (request validation)
- **PostgreSQL** with **psycopg 3** (raw SQL, no ORM)
- **pwdlib / Argon2** for password hashing
- **uv** for dependency management

## What's implemented

- `POST /auth/register`: validates the email and enforces a minimum password length of 8. It lowercases the email, hashes the password with Argon2 and stores the user. A duplicate email returns `409 Conflict`, using Postgres's unique constraint rather than a separate lookup.
- `GET /health`: liveness check.
- Schema (`backend/schema.sql`):
  - `users`
  - `applications`, which has a Postgres `ENUM` status (`applied`, `interviewing`, `offer`, `rejected`), a foreign key to `users` with `ON DELETE CASCADE`, and an index on `user_id`.

### Planned

- JWT login and protected routes
- CRUD endpoints for applications, filtered by status

## Running it locally

Requirements: Python 3.14+, [uv](https://docs.astral.sh/uv/), and a running PostgreSQL server.

```bash
git clone https://github.com/foil16/job-application-tracker.git
cd job-application-tracker/backend
uv sync

# Create the database and tables
createdb job_tracker
psql -d job_tracker -f schema.sql

# Configure the connection string (edit USER/PASSWORD to match your Postgres)
cp .env.example .env

# Start the API (run from backend/app)
cd app
uv run uvicorn main:app --reload
```

The interactive API docs are at http://127.0.0.1:8000/docs.

### Example

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "ada@example.com", "password": "password123"}'
```

```json
{"id": 1, "email": "ada@example.com", "created_at": "2026-10-28T12:36:13.967494-04:00"}
```

Registering the same email again returns `409 {"detail": "Email is already in use"}`.
