from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    resp = client.post("/api/auth/register", json={"username": "newuser", "password": "secret123"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "newuser"
    assert data["is_active"] is True


def test_register_duplicate(client: TestClient):
    client.post("/api/auth/register", json={"username": "dup", "password": "pass"})
    resp = client.post("/api/auth/register", json={"username": "dup", "password": "pass"})
    assert resp.status_code == 400


def test_login_success(client: TestClient):
    client.post("/api/auth/register", json={"username": "loginuser", "password": "pass123"})
    resp = client.post("/api/auth/login", data={"username": "loginuser", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client: TestClient):
    client.post("/api/auth/register", json={"username": "user2", "password": "correct"})
    resp = client.post("/api/auth/login", data={"username": "user2", "password": "wrong"})
    assert resp.status_code == 401


def test_me_authenticated(client: TestClient, auth_headers: dict):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"


def test_me_unauthenticated(client: TestClient):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401
