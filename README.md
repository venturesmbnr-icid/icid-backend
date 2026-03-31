
# ICID Reporting API (Skeleton)

## Run (dev)
1) Create Postgres locally and set `DATABASE_URL` in `.env` or environment.
2) Install deps: `pip install -r requirements.txt`
3) Start API: `uvicorn app.main:app --reload`
3.05) Start API: `uvicorn main:app --reload`
3.1) Start API: `uvicorn api.index:app --reload`
4) Open docs: http://localhost:8000/docs

## Notes
- Async SQLAlchemy 2.0 + asyncpg
- Tenants & Clients modeled; extend with Projects, Reports, Workflow next
- Add Alembic migrations later: `pip install alembic` and `alembic init alembic`
