from tabulate import tabulate
from api.db.connection import get_connection


def run_query(sql: str, params=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)

            if cur.description:
                rows = cur.fetchall()
                headers = [d.name for d in cur.description]

                if rows:
                    print(tabulate(rows, headers=headers, tablefmt="grid"))
                else:
                    print("Query executed but returned 0 rows.")

                return rows

            conn.commit()
            print("Query executed successfully.")
            return None
