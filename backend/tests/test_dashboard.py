from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_dashboard_stats(client: TestClient, auth_headers: dict):
    resp = client.get("/api/dashboard/stats", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "total_servers" in data
    assert "active_servers" in data


def test_kubernetes_status(client: TestClient, auth_headers: dict):
    resp = client.get("/api/kubernetes/status", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "cluster_name" in data
    assert "nodes" in data
    assert "pods" in data
