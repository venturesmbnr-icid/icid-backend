from api.db.runner import run_query


def get_all_users():
    sql = "SELECT * FROM icid.users ORDER BY last_name, first_name;"
    return run_query(sql)


def get_user_by_id(user_id: str):
    sql = "SELECT * FROM icid.users WHERE uuid = %s;"
    rows = run_query(sql, (user_id,))
    return rows[0] if rows else None
