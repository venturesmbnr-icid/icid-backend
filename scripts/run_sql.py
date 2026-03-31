import sys
from app.db.runner import run_query


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/run_sql.py "select * from icid.users;"')
        sys.exit(1)

    sql = " ".join(sys.argv[1:])
    run_query(sql)


if __name__ == "__main__":
    main()
