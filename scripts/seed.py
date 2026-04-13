"""
Seed script — inserts one test client, one test user, and three test projects,
then assigns the user to all three projects.

Run from the project root:
    conda run -p .venvICIDBackend python scripts/seed.py

Safe to run multiple times: uses INSERT ... ON CONFLICT DO NOTHING.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.db.connection import get_connection

# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

TEST_CLIENT = {
    "client_id": "C001",
    "client_username": "dev_client",
    "client_name": "Dev Agency",
    "client_email": "admin@devagency.com",
    "client_phone": "555-0100",
    "client_role": "GC",
}

TEST_USER = {
    "uuid": "00000000-0000-0000-0000-000000000001",
    "email": "dev.user@devagency.com",
    "first_name": "Dev",
    "last_name": "User",
    "phone_number": "555-0101",
    "client_id": "C001",
}

TEST_PROJECTS = [
    {
        "project_id": "P001",
        "project_name": "Brooklyn Bridge Rehabilitation",
        "project_description": "Full rehabilitation of the Brooklyn Bridge deck and cables.",
        "registration_code": "REG-2024-001",
        "borough": "Brooklyn",
        "status": "active",
    },
    {
        "project_id": "P002",
        "project_name": "Queens Plaza Streetscape Upgrade",
        "project_description": "Streetscape improvements along Queens Plaza North.",
        "registration_code": "REG-2024-002",
        "borough": "Queens",
        "status": "active",
    },
    {
        "project_id": "P003",
        "project_name": "Bronx Transit Hub Expansion",
        "project_description": "Expansion of the Bronx transit hub to add new bus lanes.",
        "registration_code": "REG-2024-003",
        "borough": "Bronx",
        "status": "pending",
    },
]

PROJECT_ASSIGNMENTS = [
    {"project_id": "P001", "user_uuid": TEST_USER["uuid"], "user_role": "inspector"},
    {"project_id": "P002", "user_uuid": TEST_USER["uuid"], "user_role": "supervisor"},
    {"project_id": "P003", "user_uuid": TEST_USER["uuid"], "user_role": "inspector"},
]


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

def seed_client(cur, client: dict):
    cur.execute(
        """
        INSERT INTO icid.clients (client_id, client_username, client_name, client_email, client_phone, client_role)
        VALUES (%(client_id)s, %(client_username)s, %(client_name)s, %(client_email)s, %(client_phone)s, %(client_role)s)
        ON CONFLICT (client_id) DO NOTHING;
        """,
        client,
    )
    print(f"  client {client['client_id']} ({client['client_name']}) — seeded")


def seed_user(cur, user: dict):
    cur.execute(
        """
        INSERT INTO icid.users (uuid, email, first_name, last_name, phone_number, client_id)
        VALUES (%(uuid)s, %(email)s, %(first_name)s, %(last_name)s, %(phone_number)s, %(client_id)s)
        ON CONFLICT (uuid) DO NOTHING;
        """,
        user,
    )
    print(f"  user {user['uuid']} ({user['email']}) — seeded")


def seed_project(cur, project: dict):
    cur.execute(
        """
        INSERT INTO icid.projects (project_id, project_name, project_description, registration_code, borough, status)
        VALUES (%(project_id)s, %(project_name)s, %(project_description)s, %(registration_code)s, %(borough)s, %(status)s)
        ON CONFLICT (project_id) DO NOTHING;
        """,
        project,
    )
    print(f"  project {project['project_id']} ({project['project_name']}) — seeded")


def seed_assignment(cur, assignment: dict):
    cur.execute(
        """
        INSERT INTO icid.project_users (project_id, user_uuid, user_role)
        VALUES (%(project_id)s, %(user_uuid)s, %(user_role)s)
        ON CONFLICT (project_id, user_uuid) DO NOTHING;
        """,
        assignment,
    )
    print(f"  assignment {assignment['project_id']} → {assignment['user_uuid']} ({assignment['user_role']}) — seeded")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Seeding database...")

    with get_connection() as conn:
        with conn.cursor() as cur:
            print("\n[1] Client")
            seed_client(cur, TEST_CLIENT)

            print("\n[2] User")
            seed_user(cur, TEST_USER)

            print("\n[3] Projects")
            for project in TEST_PROJECTS:
                seed_project(cur, project)

            print("\n[4] Project assignments")
            for assignment in PROJECT_ASSIGNMENTS:
                seed_assignment(cur, assignment)

        conn.commit()

    print("\nSeed complete.")
    print(f"\nTest user ID: {TEST_USER['uuid']}")
    print(f"Test user email: {TEST_USER['email']}")
    print("\nEndpoints to test:")
    print(f"  GET /v1/users/")
    print(f"  GET /v1/projects/?user_id={TEST_USER['uuid']}")
    print(f"  GET /v1/projects/P001")


if __name__ == "__main__":
    main()
