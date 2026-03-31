# ICID Backend – FastAPI & Uvicorn Run Guide

This document explains how to:

- Use the Python virtual environment for the project
- Install required Python packages
- Configure the database URL for the app
- Run the FastAPI app with Uvicorn
- Test the `/v1/clients` endpoints via Swagger UI

Project root:

```text
/Users/mehdis/icid-backend
```

Python virtual environment:

```text
/Users/mehdis/icid-backend/.venvICID
```

---

## 1. Activate the virtual environment

From the project root:

```bash
cd /Users/mehdis/icid-backend
conda activate /Users/mehdis/icid-backend/.venvICID
```

(Alternatively, if it’s a plain venv: `source .venvICID/bin/activate`.)

Your shell prompt should show:

```text
(/Users/mehdis/icid-backend/.venvICID) ...
```

---

## 2. Install Python dependencies

We are using:

- `fastapi` – web framework
- `uvicorn` – ASGI server
- `sqlalchemy` – ORM
- `asyncpg` – async PostgreSQL driver
- `pydantic` – request/response validation
- `email-validator` – required for `EmailStr` fields

Install them (inside the venv):

```bash
pip install fastapi uvicorn[standard] sqlalchemy asyncpg pydantic email-validator
```

If you maintain a `requirements.txt`, you can also do:

```bash
pip install -r requirements.txt
```

---

## 3. Configure the database URL

The app uses SQLAlchemy’s async engine with `asyncpg`. The connection URL format is:

```text
postgresql+asyncpg://USER[:PASSWORD]@HOST:PORT/DBNAME
```

For local development on this machine:

- User: `mehdis`
- Host: `localhost`
- DB: `icid`
- Port: `5432`

No password example:

```bash
export DATABASE_URL="postgresql+asyncpg://mehdis@localhost:5432/icid"
```

If you add a password to the `mehdis` role:

```bash
export DATABASE_URL="postgresql+asyncpg://mehdis:YOUR_PASSWORD@localhost:5432/icid"
```

You can add this line to your shell profile (e.g. `~/.zshrc`) so it’s available automatically when you open a terminal.

The app reads this in something like `app/core/config.py`:

```python
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()
```

And the async engine is created in `app/db/session.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 4. Project structure (relevant parts)

Rough relevant layout:

```text
icid-backend/
  app/
    main.py
    api/
      v1/
        clients.py
    models/
      client.py
    schemas/
      client.py
    crud/
      client.py
    db/
      base.py
      session.py
  schema.sql
```

Key components:

- `app/main.py` – FastAPI application entry point
- `app/api/v1/clients.py` – `/v1/clients` router
- `app/models/client.py` – SQLAlchemy `Client` model
- `app/schemas/client.py` – Pydantic `ClientCreate` and `ClientRead`
- `app/crud/client.py` – CRUD logic using async SQLAlchemy
- `app/db/session.py` – async engine and session factory

---

## 5. Starting the FastAPI server with Uvicorn

From the project root, with venv active and `DATABASE_URL` set:

```bash
uvicorn app.main:app --reload
```

Expected startup logs:

```text
INFO:     Will watch for changes in these directories: ['/Users/mehdis/icid-backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [yyyyy]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The `--reload` flag enables auto-reload when code changes (dev mode).

---

## 6. Swagger UI – exploring the API

Open a browser and go to:

- **Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

You should see the interactive Swagger UI including at least:

- `GET /v1/clients/`
- `POST /v1/clients/`

---

## 7. Example: creating a client

In Swagger UI:

1. Click `POST /v1/clients/`

2. Click **“Try it out”**

3. Example request body:

   ```json
   {
     "client_id": "C00046",
     "client_username": "client_c00046",
     "client_name": "Test Client 2",
     "client_email": "test2@example.com",
     "client_phone": "555-9999",
     "client_role": "GC"
   }
   ```

4. Click **“Execute”**

If everything is configured correctly, you should get `201 Created` and a response like:

```json
{
  "id": "84974f04-b7cf-4c85-b78b-f9602fadab54",
  "client_id": "C00046",
  "client_username": "client_c00046",
  "client_name": "Test Client 2",
  "client_email": "test2@example.com",
  "client_phone": "555-9999",
  "client_role": "GC"
}
```

---

## 8. Example: listing all clients

In Swagger UI:

1. Click `GET /v1/clients/`
2. Click **“Try it out”**, then **“Execute”**

Example response:

```json
[
  {
    "id": "84974f04-b7cf-4c85-b78b-f9602fadab54",
    "client_id": "C00046",
    "client_username": "client_c00046",
    "client_name": "Test Client 2",
    "client_email": "test2@example.com",
    "client_phone": "555-9999",
    "client_role": "GC"
  },
  {
    "id": "1935f8c9-2cb7-4402-87f8-50b754539afc",
    "client_id": "C00045",
    "client_username": "Magnol_Eng",
    "client_name": "Magnol Engineering PC",
    "client_email": "Admin@magnoleng.pc",
    "client_phone": "(718) 024-6888",
    "client_role": "Consultant"
  }
]
```

This shows:

- Data is persisted in the `icid` PostgreSQL database.
- The `/v1/clients` API is wired end-to-end (FastAPI ⇄ SQLAlchemy ⇄ Postgres).

---

## 9. Handling common issues

### 9.1. `asyncpg.exceptions.InvalidAuthorizationSpecificationError: role "postgres" does not exist`

Cause: `DATABASE_URL` is using user `postgres`, but the local role is `mehdis`.

Fix: Update `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql+asyncpg://mehdis@localhost:5432/icid"
```

Restart Uvicorn.

---

### 9.2. `ModuleNotFoundError: No module named 'asyncpg'`

Cause: `asyncpg` not installed in the venv.

Fix:

```bash
pip install asyncpg
```

---

### 9.3. `ImportError: email-validator is not installed, run 'pip install pydantic[email]'`

Cause: Using `EmailStr` in Pydantic schemas without `email-validator` installed.

Fix:

```bash
pip install email-validator
```

---

### 9.4. Pydantic response validation error: `value is not a valid dict`

Cause: Returning ORM models without `orm_mode`.

Fix schema:

```python
class ClientRead(BaseModel):
    ...
    class Config:
        orm_mode = True
```

---

## 10. Stopping the server

To stop the dev server:

- Go to the terminal where Uvicorn is running.
- Press `CTRL + C`.

---

## 11. Summary

Daily workflow to run the backend:

```bash
cd /Users/mehdis/icid-backend
conda activate /Users/mehdis/icid-backend/.venvICID
export DATABASE_URL="postgresql+asyncpg://mehdis@localhost:5432/icid"
uvicorn app.main:app --reload
```

Then:

- Open `http://127.0.0.1:8000/docs`
- Use the interactive docs to test `/v1/clients` and (later) other endpoints.

This is the standard way to bring up the ICID backend on a local machine.
