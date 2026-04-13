from api.db.runner import run_query


def get_all_users():
    sql = """
        SELECT
            u.user_id,
            u.email,
            u.first_name,
            u.last_name,
            u.phone_number,
            c.client_name AS employer
        FROM icid.users u
        LEFT JOIN icid.clients c ON u.employer = c.client_id
        ORDER BY u.last_name, u.first_name;
    """
    return run_query(sql)


def get_user_by_id(user_id: int):
    sql = """
        SELECT
            u.user_id,
            u.email,
            u.first_name,
            u.last_name,
            u.phone_number,
            c.client_name AS employer
        FROM icid.users u
        LEFT JOIN icid.clients c ON u.employer = c.client_id
        WHERE u.user_id = %s;
    """
    rows = run_query(sql, (user_id,))
    return rows[0] if rows else None
