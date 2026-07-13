# Task Management API

A Task Management REST API built with **FastAPI** and **PostgreSQL** as a project-based learning journey into backend development and application security (AppSec).

Built by a frontend engineer (Angular) transitioning into full-stack + AppSec.

## Stack

- **Python 3.14+** (managed with [uv](https://docs.astral.sh/uv/))
- **FastAPI** — web framework
- **Pydantic v2** — request/response validation
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL** — database
- **psycopg2** — PostgreSQL driver

## Current Status

✅ **Phase 3C complete** — Full CRUD (Create / Read all / Read one / Update / Delete) backed by PostgreSQL.

See [`docs/learning-notes.md`](docs/learning-notes.md) for the full learning roadmap, concepts covered, and AppSec debrief.

## Endpoints

| Method | Path          | Purpose        |
| ------ | ------------- | -------------- |
| POST   | `/tasks/`     | Create a task  |
| GET    | `/tasks/`     | List all tasks |
| GET    | `/tasks/{id}` | Get one task   |
| PUT    | `/tasks/{id}` | Update a task  |
| DELETE | `/tasks/{id}` | Delete a task  |

Interactive docs (Swagger UI) available at `/docs` when the app is running.

## Local Setup

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) installed
- PostgreSQL running locally (Homebrew on macOS is fine)
- A database named `taskdb` created

### Environment Variables

Create a `.env` file at the project root (not committed):

```env
APP_NAME=Task API
DEBUG=true
API_VERSION=v1
DATABASE_URL=postgresql+psycopg2://your_mac_username@localhost:5432/taskdb
```

### Install dependencies

```bash
uv sync
```

### Create the `tasks` table

In DBeaver (or psql), run:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
```

### Run the app

```bash
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints.

## Project Structure

```
app/
├── core/config.py             # Pydantic Settings (loaded from .env)
├── db/
│   ├── base.py                # SQLAlchemy DeclarativeBase
│   └── session.py             # Engine, SessionLocal, get_db dependency
├── models/task.py             # SQLAlchemy Task model
├── routers/tasks.py           # HTTP endpoints
├── schemas/task.py            # Pydantic request/response models
├── services/task_service.py   # Business logic + DB operations
└── main.py                    # FastAPI app entry point
```

## Learning Notes

The full learning journey — concepts, mental models, security debriefs, and roadmap — lives in [`docs/learning-notes.md`](docs/learning-notes.md).

## Security Note

This project is a learning sandbox. It intentionally does **not** yet include authentication, authorization, HTTPS, rate limiting, or logging — those are upcoming phases. **Do not deploy this as-is.** See the "Known Latent Issues" section in the learning notes for the full list.
