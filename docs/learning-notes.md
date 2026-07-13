# Backend Development Learning Roadmap Notes

**Project:** Task Management API
**Stack:** Python, FastAPI, uv, PostgreSQL, SQLAlchemy, DBeaver, later Alembic, JWT, Docker, CI/CD, and cybersecurity practices

---

## Big Picture

The goal of this course is not to build separate mini-projects. The goal is to build **one evolving project** that starts simple and gradually becomes a production-style backend system.

Your long-term project is:

> **Task Management API**

By the end of the full roadmap, this project should include:

- CRUD operations
- Clean FastAPI project structure
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- Request and response models
- Authentication
- Authorization
- JWT security
- Password hashing
- Testing
- Docker
- CI/CD
- Deployment readiness
- Cybersecurity awareness and secure coding practices

---

# Phase 1 — FastAPI Fundamentals

## Goal

Phase 1 focused on understanding how APIs work using FastAPI. We intentionally avoided PostgreSQL, SQLAlchemy, authentication, and Docker so the fundamentals are easier to understand.

Flow:

```text
HTTP Request → FastAPI Route → Python Function → Temporary In-Memory Data → JSON Response
```

## What We Built

First version of the Task Management API using FastAPI, Pydantic, an in-memory list (`tasks = []`), CRUD endpoints, and Swagger UI.

## Main Concepts Learned

- **FastAPI Application** — `app = FastAPI()` receives HTTP requests and routes them.
- **Routes and Endpoints** — `@app.get("/")` maps a URL + method to a Python function.
- **CRUD and HTTP Methods** — POST/GET/PUT/DELETE map to Create/Read/Update/Delete.
- **Pydantic Model** — defines expected shape of data; FastAPI validates request bodies automatically.
- **In-Memory Storage** — `tasks = []` for learning; data is lost on restart (motivation for PostgreSQL later).
- **HTTPException** — `raise HTTPException(status_code=404, detail="Task not found")` returns proper HTTP errors so frontends (like Angular) can react correctly.
- **response_model** — declares response shape; improves Swagger docs and consistency.
- **Query Parameters and Filtering** — e.g., `?completed=true`.
- **Annotated** — `Annotated[TYPE, METADATA]` = "this is TYPE with extra instructions for FastAPI." Foundation for `Depends`, `Query`, `Path`, etc.

## Phase 1.1 — Cleaner FastAPI API

Improved Phase 1 with `HTTPException`, `response_model`, filtering, and modern `Annotated` syntax.

---

# Phase 2 — Project Structure, Configuration, and Architecture Foundations

## Phase 2A — Project Structure

Moved from a single `main.py` into a layered structure:

```text
task-api/
└── app/
    ├── main.py
    ├── routers/tasks.py       ← Which URL calls which logic?
    ├── schemas/task.py        ← What should data look like?
    └── services/task_service.py ← What should the application do?
```

Request flow:

```text
Request → Router → Service → Data → Response
```

## Phase 2B — Python Imports, Modules, and Packages

- A file = module. A folder with modules = package.
- `from app.schemas.task import TaskCreate` = go to `app/schemas/task.py` and import `TaskCreate`.
- Angular analogy: same as `import { TaskService } from './services/task.service';`

## Phase 2C — Configuration and Environment Variables

- Separate config from code using a `.env` file + `pydantic-settings`.
- `.env` uses `UPPERCASE`, Python uses `snake_case` — Pydantic maps them automatically.
- Never hardcode secrets. `.env` must be in `.gitignore`.

## Phase 2D — Request/Response Models & Dependency Injection Foundation

- Separate `TaskCreate` (what clients can send) from `TaskResponse` (what backend returns).
- Prevents **mass assignment** — client can't sneak in fields like `id: 999` or `is_admin: true`.
- Introduced `Depends()` as "FastAPI, please provide this thing for me." Mental foundation for `db: Annotated[Session, Depends(get_db)]`.

---

# Cybersecurity Track

Every major feature is studied from three views:

```text
Developer View — How do we build it?
Attacker View — How could this be abused?
Defensive View — How do we secure it?
```

Topics threaded throughout: input validation, information disclosure, SQL injection, mass assignment, broken access control, IDOR, auth weaknesses, password hashing, JWT security, secrets management, dependency risks, CI/CD secret exposure, secure deployment.

---

# Phase 3 — PostgreSQL, SQLAlchemy, and Database Integration

## Phase 3A — PostgreSQL Fundamentals

Replaced in-memory storage with a real database.

### Setup Notes

- On macOS/Homebrew Postgres, the default role is your macOS username (not `postgres`). This is why our `DATABASE_URL` uses the Mac username.
- In DBeaver, enabled "Show all databases" to create `taskdb`.

### Table Created

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
```

### CRUD ↔ HTTP ↔ SQL Mapping

| Action   | API                | SQL                                 |
| -------- | ------------------ | ----------------------------------- |
| Create   | POST /tasks        | INSERT INTO tasks ...               |
| Read all | GET /tasks         | SELECT \* FROM tasks                |
| Read one | GET /tasks/{id}    | SELECT \* FROM tasks WHERE id = ... |
| Update   | PUT /tasks/{id}    | UPDATE tasks SET ... WHERE id = ... |
| Delete   | DELETE /tasks/{id} | DELETE FROM tasks WHERE id = ...    |

## Phase 3B — SQLAlchemy Setup

Installed `sqlalchemy` and `psycopg2-binary`:

```text
FastAPI → SQLAlchemy → psycopg2 → PostgreSQL
```

### DATABASE_URL Anatomy

```text
postgresql+psycopg2://your_mac_username@localhost:5432/taskdb
│         │  │        │                │         │    │
dialect   +  driver   user             host      port database
```

Sources:

- `dialect+driver://` format → **SQLAlchemy** URL spec
- `postgresql://` scheme → **PostgreSQL** libpq spec
- `5432` → PostgreSQL default port (IANA)
- Mac username → **Homebrew's** default role behavior

### Files Created

- `app/db/base.py` — `class Base(DeclarativeBase)` — SQLAlchemy 2.0 modern style; central registry for all models.
- `app/db/session.py` — engine + `SessionLocal` factory + `get_db()` dependency with `yield`/`try`/`finally` for guaranteed cleanup (prevents connection leaks → DoS defense).
- `app/models/task.py` — SQLAlchemy `Task` model with `Mapped[...]` type hints and `mapped_column(...)`.

### The Three-Way Alignment

```text
PostgreSQL Table (physical storage)
       ↓ maps to
SQLAlchemy Model (Python ↔ DB bridge)
       ↓ converted to
Pydantic Schema (public API contract)
```

Same shape, different concerns. Will diverge later (e.g., DB has `password_hash`, response schema must never expose it).

### `mapped_column()` Argument Rules

- The SQL type (`Integer`, `Text`, `Boolean`) is **optional** in SQLAlchemy 2.0 — can be inferred from `Mapped[...]`, but convention is to always pass it explicitly as the first positional arg.
- Keyword args (`primary_key=`, `nullable=`, `default=`, `index=`) can be in any order.
- Positional args must come before keyword args (Python rule).
- Recommended order: SQL type → structural (`primary_key`) → constraints (`nullable`, `unique`) → defaults (`default`) → performance hints (`index`).

---

# Phase 3C — Complete FastAPI + PostgreSQL CRUD ✅

## Goal

Replace the in-memory list with fully database-backed CRUD across all five endpoints.

## Final Endpoint Surface

| Method | Endpoint      | Purpose               | Status Code          |
| ------ | ------------- | --------------------- | -------------------- |
| POST   | `/tasks/`     | Create                | 201 Created          |
| GET    | `/tasks/`     | Read all              | 200 OK               |
| GET    | `/tasks/{id}` | Read one              | 200 OK / 404         |
| PUT    | `/tasks/{id}` | Update (full replace) | 200 OK / 404         |
| DELETE | `/tasks/{id}` | Delete                | 204 No Content / 404 |

## The Full Request Journey

```text
1. Client (Swagger / Angular / Postman)
   POST /tasks + JSON body
       ↓ HTTP
2. FastAPI receives, validates body with TaskCreate schema
   Calls get_db() → fresh SQLAlchemy session
       ↓
3. Router calls service function with db + task_data
       ↓
4. Service:
   - Builds SQLAlchemy Task object
   - db.add()      → stage insert
   - db.commit()   → send to PostgreSQL
   - db.refresh()  → re-read to get generated id
       ↓
5. FastAPI serializes Task → TaskResponse (Pydantic) → JSON
       ↓
6. get_db() resumes → db.close() (via finally)
       ↓
7. Client receives 201 Created + JSON body
```

## Key Concepts Learned

### Dependency Injection with `Annotated`

```python
db: Annotated[Session, Depends(get_db)]
```

Reads as: "This parameter is a `Session`, and FastAPI should get it by calling `get_db()`."

Angular analogy: like `constructor(private taskService: TaskService)` — the framework provides the dependency.

### Session Lifecycle with `yield`

```python
def get_db():
    db = SessionLocal()
    try:
        yield db          # hand session to endpoint, PAUSE
    finally:
        db.close()        # ALWAYS runs, even on exceptions
```

`try/finally` prevents **connection leaks** — a DoS vulnerability class where a leaky endpoint slowly exhausts the DB connection pool.

### SQLAlchemy Object States

| State      | Meaning                                  | Example                       |
| ---------- | ---------------------------------------- | ----------------------------- |
| Transient  | New Python object, not tracked           | `Task(title="x")`             |
| Pending    | `db.add()` called, will INSERT on commit | after `db.add(new_task)`      |
| Persistent | Fetched from DB, session tracks changes  | after `db.query(...).first()` |

**Rule:** `db.add()` is only needed for **new** objects. For **existing** objects (fetched from DB), just modify attributes and commit — the session already tracks them.

### The `add → commit → refresh` Pattern (for INSERT)

```python
db.add(new_task)      # stage
db.commit()           # persist
db.refresh(new_task)  # sync back DB-generated values (id, timestamps, etc.)
```

### Query Chain Pattern

```python
db.query(Task).filter(Task.id == task_id).first()
```

- `.first()` → first match or `None` (perfect for lookups by unique fields)
- `.all()` → list of matches (possibly empty)
- `.one()` → exactly one, else raises exception

Note: `Task.id == task_id` uses Python operator overloading — SQLAlchemy translates it to a parameterized SQL `WHERE tasks.id = ?`, safely.

### UPDATE Pattern (in-place modification)

```python
task = db.query(Task).filter(Task.id == task_id).first()
task.title = task_data.title           # explicit field-picking
task.description = task_data.description
task.completed = task_data.completed
db.commit()
db.refresh(task)
```

No `db.add()` needed — session already tracks fetched objects (persistent state).

### DELETE Pattern

```python
task = db.query(Task).filter(Task.id == task_id).first()
db.delete(task)
db.commit()
```

Currently a **hard delete** (row is gone forever). Real production apps often use **soft delete** (a `deleted_at` column) for audit trail and GDPR compliance.

### HTTP Status Codes Used

| Code                     | Meaning                | When                  |
| ------------------------ | ---------------------- | --------------------- |
| 200 OK                   | Success with body      | GET, PUT              |
| 201 Created              | New resource created   | POST                  |
| 204 No Content           | Success, no body       | DELETE                |
| 404 Not Found            | Resource doesn't exist | Any lookup miss       |
| 422 Unprocessable Entity | Validation failed      | Automatic (bad input) |

Best practice: use `status.HTTP_404_NOT_FOUND` (named constants) instead of raw numbers — self-documenting, IDE-friendly, harder to typo.

### The DELETE Response Quirk

DELETE returns 204 with an **empty body** (HTTP spec). Because FastAPI defaults to JSON serialization, we need:

```python
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,   # don't JSON-serialize
)
def remove_task(...):
    ...
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

### Path Parameters + Auto-Validation

```python
@router.get("/{task_id}")
def get_task(task_id: int, ...):
    ...
```

FastAPI extracts `task_id` from the URL and validates it's an integer. Sending `/tasks/hello` returns 422 automatically — no manual validation code needed. This is your **first line of defense** at the input boundary.

### `from_attributes=True` on Response Schemas

```python
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ...
```

Allows Pydantic to read attributes off SQLAlchemy objects (which use `.title`, not `["title"]`). This is the bridge between the ORM world and the API world. Modern Pydantic v2 syntax (older `class Config: from_attributes = True` still works but is deprecated style).

### Router-Level Prefix and Tags

```python
router = APIRouter(prefix="/tasks", tags=["tasks"])
```

- `prefix` → applied to every route (cleaner than repeating `/tasks` per decorator; easier to version later like `/api/v1/tasks`).
- `tags` → groups endpoints in Swagger UI.

---

# Phase 3C — Security Debrief 🛡️

## OWASP Top 10 Coverage (as of Phase 3C)

| #   | OWASP Category            | Status                                               |
| --- | ------------------------- | ---------------------------------------------------- |
| A01 | Broken Access Control     | ❌ Not implemented (Phase 5)                         |
| A02 | Cryptographic Failures    | ⚠️ Latent (no HTTPS, no password hashing yet)        |
| A03 | Injection                 | ✅ **Defended** via SQLAlchemy parameterized queries |
| A04 | Insecure Design           | ✅ Layered architecture, explicit boundaries         |
| A05 | Security Misconfiguration | ⚠️ `DEBUG=true`, DB superuser, open Swagger          |
| A06 | Vulnerable Components     | ⚠️ No dependency scanning yet (Phase 8)              |
| A07 | Auth Failures             | ❌ Not implemented (Phase 4)                         |
| A08 | Software/Data Integrity   | ⚠️ Supply chain awareness pending (Phase 8)          |
| A09 | Logging & Monitoring      | ❌ No logging yet                                    |
| A10 | SSRF                      | ✅ N/A (no outbound HTTP yet)                        |

## What's Defended

### 1. SQL Injection (CWE-89) ✅

Every query uses SQLAlchemy's parameterized query mechanism. Even `Task.id == task_id` in a filter translates to a parameterized SQL `WHERE tasks.id = ?`. Values are never mixed into the SQL string.

**Danger zones to watch:** `db.execute(text(f"..."))` with f-strings, `LIKE` queries with unescaped `%`/`_`, order-by clauses with dynamic column names (ORMs don't parameterize identifiers).

### 2. Mass Assignment (CWE-915) ✅ (double-defended)

- **Layer 1:** Pydantic schemas explicitly list allowed fields. Client can't send `id` or (in create) `completed`.
- **Layer 2:** Service layer picks fields explicitly: `task.title = task_data.title`. No `for key, value in data.dict().items(): setattr(...)` blind copy.

Real-world precedent: GitHub itself had this bug in 2012 — someone escalated to admin via an extra field in a user-update request.

### 3. Information Disclosure (CWE-200) ✅

Error messages say the minimum: `"Task not found"` — not `"Task with id 42 not found in taskdb.public.tasks"`. No schema, no user PII, no SQL leaked.

### 4. Secrets Management ✅

- `.env` for secrets, `.gitignore` excludes it.
- App refuses to start without `DATABASE_URL` — fail-fast, fail-secure.

### 5. Input Validation ✅

- Path parameters typed (`task_id: int`) — non-integers rejected at boundary with 422.
- Request bodies validated by Pydantic schemas.

### 6. Resource Leak Prevention ✅

`try/finally` in `get_db()` guarantees `db.close()` runs even on exceptions.

## Known Latent Issues (Planned for Future Phases)

### 1. Broken Access Control (A01) — Phase 4/5

Any client that can reach the API can CRUD any task. No login, no ownership.

**IDOR (Insecure Direct Object Reference, CWE-639):** Once users exist, if Alice can `GET /tasks/42` and see Bob's task, that's IDOR. Fix: ownership check + return 404 (not 403) to avoid confirming existence.

### 2. Unbounded Queries (CWE-770) — Latent DoS

```python
db.query(Task).all()   # ← returns EVERY row
```

If the table grows to 10M rows, one request tries to load 10M objects. Fix: pagination with `.limit()` / `.offset()`. Every list-returning endpoint is a potential DoS vector.

### 3. Security Misconfiguration (A05)

- `DEBUG=true` should be `false` in production.
- Swagger UI at `/docs` should be auth-protected or disabled in production (it's a full attack map of your API otherwise).

### 4. Principle of Least Privilege

App connects as macOS user = PostgreSQL **superuser**. If compromised, attacker can `DROP DATABASE`, read every DB, create users. In production: create a dedicated DB user with only `SELECT/INSERT/UPDATE/DELETE` on `tasks` table.

### 5. No Authentication (A07) — Phase 4

Everything below is TODO:

- User model + registration
- Password hashing (bcrypt/argon2 — NEVER plain text or MD5/SHA1)
- Login endpoint
- JWT token generation + validation
- OAuth2 password flow
- Current user dependency

### 6. No Logging (A09)

No audit trail of who did what and when. Needed for both operations and security incident response.

## AppSec Mental Model (Reinforced)

Every input from outside is untrusted. Every response leak is intel for attackers. Every extra permission is extra risk.

Three-view checklist per feature:

- **Developer:** How does it work?
- **Attacker:** How could it be abused?
- **Defender:** What layer of defense prevents that abuse?

Defense-in-depth: multiple overlapping controls. One missing control shouldn't equal a breach.

---

# Future Phases

## Phase 3D — Alembic Migrations

Version-control database schema changes. Prevents manual DBeaver edits from getting out of sync across dev/staging/prod. Mental model: **Git for your database schema**.

## Phase 3E — Database Relationships

Add `users` table. Foreign key from `tasks` to `users`. One-to-many: user has many tasks. **Prerequisite for authentication.**

## Phase 4 — Authentication

User registration, login, password hashing, JWT, OAuth2 password flow, current-user dependency. AppSec focus: never store plaintext passwords, hashing vs encryption, brute-force protection, credential stuffing.

## Phase 5 — Authorization

Task ownership checks. Only owners can update/delete. Admin vs regular user. Role-based access control basics. AppSec focus: broken access control, IDOR, mass assignment, privilege escalation.

## Phase 6 — Testing

pytest, FastAPI TestClient, test database setup, testing CRUD/auth/authz. AppSec focus: tests for unauthorized access, invalid input, forbidden actions.

## Phase 7 — Docker

Dockerfile, docker-compose, containerize FastAPI + PostgreSQL, environment variables in containers, volumes. AppSec focus: don't bake secrets into images, container isolation basics.

## Phase 8 — CI/CD

GitHub Actions: automated tests, linting, build checks, dependency install with uv, deployment pipeline. AppSec focus: CI/CD secret exposure, dependency risk, supply chain awareness.

## Phase 9 — Deployment and Cloud Database

Deploy the app, connect to cloud PostgreSQL (Supabase or similar). Production `DATABASE_URL`, CORS, prod settings, logging. AppSec focus: production secrets, HTTPS, DB connection security, least-privilege DB users.

## Phase 10 — Security Review and Mini Pen Test

Review the completed project through OWASP Top 10 lens: SQL injection, auth, authz, IDOR, error handling, secrets, dependencies. Ethical, defensive learning in the owner's own lab environment only.

---

# Learning Style Cycle

For each phase:

```text
1. Learn the concept
2. See the visual flow
3. Write the code
4. Test in Swagger
5. Verify in DBeaver or logs
6. Discuss security implications
7. Refactor if needed
```

---

# Quick Concept Map

```text
Frontend / Swagger / Client
        ↓
FastAPI Router
        ↓
Pydantic Request Schema (validate input)
        ↓
Dependency Injection (get_db, later: current_user)
        ↓
Service Layer (business logic)
        ↓
SQLAlchemy Session
        ↓
SQLAlchemy Model
        ↓
PostgreSQL Table
        ↓
Pydantic Response Schema (shape output)
        ↓
JSON Response
```

---

# Final Reminder

Not just learning FastAPI — building the foundation to be a:

```text
Backend Developer + Security-Aware Developer (AppSec-oriented)
```

Especially valuable combined with existing Angular frontend experience — the full stack is visible:

```text
Angular frontend
    ↓
FastAPI backend
    ↓
PostgreSQL database
    ↓
Security controls wrapping the whole system
```
