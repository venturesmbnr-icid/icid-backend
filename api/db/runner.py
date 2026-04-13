from api.db.connection import get_connection


def run_query(sql: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)

            if cur.description:
                return cur.fetchall()

            conn.commit()
            return None
