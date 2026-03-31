from api.db.runner import run_query


def get_all_users():
    return run_query("select * from icid.users;")


def get_user_by_id(user_id):
    return run_query("select * from icid.users where id = %s;", (user_id,))
