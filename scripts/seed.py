"""
Seed script — inserts test data matching the actual icid schema in Neon.

Run from the project root:
    conda run -p .venvICIDBackend python scripts/seed.py

Safe to run multiple times: uses INSERT ... ON CONFLICT DO NOTHING.

Dev user ID: 28 (Genghis Khan — already in DB)
Test projects will be assigned to user_id 28.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.db.connection import get_connection

# ---------------------------------------------------------------------------
# Seed data — matches actual icid schema
# ---------------------------------------------------------------------------

# Use an existing user from the DB (user_id 28 = Genghis Khan)
DEV_USER_ID = 28

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
    {"project_id": "P001", "user_id": DEV_USER_ID, "user_role": "inspector"},
    {"project_id": "P002", "user_id": DEV_USER_ID, "user_role": "supervisor"},
    {"project_id": "P003", "user_id": DEV_USER_ID, "user_role": "inspector"},
]


# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

def seed_project(cur, project: dict):
    cur.execute(
        """
        INSERT INTO icid.projects
            (project_id, project_name, project_description, registration_code, borough, status)
        VALUES
            (%(project_id)s, %(project_name)s, %(project_description)s,
             %(registration_code)s, %(borough)s, %(status)s)
        ON CONFLICT (project_id) DO NOTHING;
        """,
        project,
    )
    print(f"  project {project['project_id']} ({project['project_name']}) — seeded")


def seed_assignment(cur, assignment: dict):
    cur.execute(
        """
        INSERT INTO icid.project_user (project_id, user_id, user_role)
        VALUES (%(project_id)s, %(user_id)s, %(user_role)s)
        ON CONFLICT (project_id, user_id) DO NOTHING;
        """,
        assignment,
    )
    print(f"  assignment {assignment['project_id']} → user {assignment['user_id']} ({assignment['user_role']}) — seeded")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Seeding database...")
    print(f"Dev user: user_id={DEV_USER_ID} (Genghis Khan)")

    with get_connection() as conn:
        with conn.cursor() as cur:
            print("\n[1] Projects")
            for project in TEST_PROJECTS:
                seed_project(cur, project)

            print("\n[2] Project assignments")
            for assignment in PROJECT_ASSIGNMENTS:
                seed_assignment(cur, assignment)

        conn.commit()

    print("\nSeed complete.")
    print(f"\nTest endpoints:")
    print(f"  GET /v1/users/")
    print(f"  GET /v1/projects/?user_id={DEV_USER_ID}")
    print(f"  GET /v1/projects/P001")


if __name__ == "__main__":
    main()
