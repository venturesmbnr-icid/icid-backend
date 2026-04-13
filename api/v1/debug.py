from fastapi import APIRouter
from api.db.runner import run_query

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/schema")
def get_schema():
    """
    List all tables and their columns in the icid schema.
    Dev-only endpoint — remove before production.
    """
    tables_sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'icid'
        ORDER BY table_name;
    """
    tables = run_query(tables_sql) or []

    result = {}
    for (table_name,) in tables:
        columns_sql = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'icid' AND table_name = %s
            ORDER BY ordinal_position;
        """
        cols = run_query(columns_sql, (table_name,)) or []
        result[table_name] = [{"column": col, "type": dtype} for col, dtype in cols]

    return {"schema": "icid", "tables": result}
