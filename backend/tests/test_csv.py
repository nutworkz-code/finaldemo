import io

from fastapi.testclient import TestClient


def test_csv_upload_success(client: TestClient, auth_headers: dict):
    csv_content = "hostname,ip_address,os,environment,status\ncsv-host-1,10.0.0.10,Ubuntu,staging,active\n"
    files = {"file": ("servers.csv", io.BytesIO(csv_content.encode()), "text/csv")}
    resp = client.post("/api/csv/upload", files=files, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["created"] == 1
    assert data["skipped"] == 0


def test_csv_upload_missing_columns(client: TestClient, auth_headers: dict):
    csv_content = "hostname,os\nhost1,Ubuntu\n"
    files = {"file": ("bad.csv", io.BytesIO(csv_content.encode()), "text/csv")}
    resp = client.post("/api/csv/upload", files=files, headers=auth_headers)
    assert resp.status_code == 400


def test_csv_upload_invalid_extension(client: TestClient, auth_headers: dict):
    files = {"file": ("data.txt", io.BytesIO(b"some data"), "text/plain")}
    resp = client.post("/api/csv/upload", files=files, headers=auth_headers)
    assert resp.status_code == 400
