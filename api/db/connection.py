import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL not found. Create a .env file in repo root."
        )

    return psycopg.connect(database_url)
