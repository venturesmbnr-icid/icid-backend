from unittest.mock import patch

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

MOCK_USER_ROWS = [
    (
        "00000000-0000-0000-0000-000000000001",
        "alice@example.com",
        "Alice",
        "Smith",
        "555-0001",
        "Acme Corp",
    ),
    (
        "00000000-0000-0000-0000-000000000002",
        "bob@example.com",
        "Bob",
        "Jones",
        "555-0002",
        "BuildCo",
    ),
]


# ---------------------------------------------------------------------------
# GET /v1/users/
# ---------------------------------------------------------------------------

class TestListAllUsers:
    def test_returns_200(self, client):
        with patch("api.queries.users.run_query", return_value=MOCK_USER_ROWS):
            response = client.get("/v1/users/")
        assert response.status_code == 200

    def test_response_shape(self, client):
        with patch("api.queries.users.run_query", return_value=MOCK_USER_ROWS):
            data = client.get("/v1/users/").json()
        assert data["status"] == "success"
        assert "message" in data
        assert isinstance(data["data"], list)

    def test_user_fields_present(self, client):
        with patch("api.queries.users.run_query", return_value=MOCK_USER_ROWS):
            users = client.get("/v1/users/").json()["data"]
        for user in users:
            assert "user_id" in user
            assert "email" in user
            assert "first_name" in user
            assert "last_name" in user
            assert "phone_number" in user
            assert "employer" in user

    def test_returns_correct_count(self, client):
        with patch("api.queries.users.run_query", return_value=MOCK_USER_ROWS):
            users = client.get("/v1/users/").json()["data"]
        assert len(users) == 2

    def test_user_id_is_string(self, client):
        with patch("api.queries.users.run_query", return_value=MOCK_USER_ROWS):
            users = client.get("/v1/users/").json()["data"]
        assert isinstance(users[0]["user_id"], str)

    def test_empty_list(self, client):
        with patch("api.queries.users.run_query", return_value=[]):
            data = client.get("/v1/users/").json()
        assert data["status"] == "success"
        assert data["data"] == []

    def test_db_failure_returns_500(self, client):
        with patch("api.queries.users.run_query", return_value=None):
            response = client.get("/v1/users/")
        assert response.status_code == 500
