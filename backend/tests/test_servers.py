from fastapi.testclient import TestClient

SERVER_PAYLOAD = {
    "hostname": "web-01",
    "ip_address": "10.0.0.1",
    "os": "Ubuntu 22.04",
    "environment": "production",
    "status": "active",
}


def test_create_server(client: TestClient, auth_headers: dict):
    resp = client.post("/api/servers/", json=SERVER_PAYLOAD, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["hostname"] == "web-01"


def test_list_servers(client: TestClient, auth_headers: dict):
    client.post("/api/servers/", json=SERVER_PAYLOAD, headers=auth_headers)
    resp = client.get("/api/servers/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_get_server(client: TestClient, auth_headers: dict):
    create = client.post("/api/servers/", json=SERVER_PAYLOAD, headers=auth_headers)
    server_id = create.json()["id"]
    resp = client.get(f"/api/servers/{server_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["hostname"] == "web-01"


def test_update_server(client: TestClient, auth_headers: dict):
    create = client.post("/api/servers/", json=SERVER_PAYLOAD, headers=auth_headers)
    server_id = create.json()["id"]
    resp = client.put(f"/api/servers/{server_id}", json={"status": "inactive"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "inactive"


def test_delete_server(client: TestClient, auth_headers: dict):
    create = client.post("/api/servers/", json=SERVER_PAYLOAD, headers=auth_headers)
    server_id = create.json()["id"]
    resp = client.delete(f"/api/servers/{server_id}", headers=auth_headers)
    assert resp.status_code == 204
