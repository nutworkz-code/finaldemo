import { useEffect, useState } from "react";
import api from "../services/api";

interface Server {
  id: number;
  hostname: string;
  ip_address: string;
  os: string | null;
  environment: string | null;
  status: string;
  description: string | null;
}

const EMPTY: Omit<Server, "id"> = {
  hostname: "",
  ip_address: "",
  os: "",
  environment: "",
  status: "active",
  description: "",
};

export default function ServersPage() {
  const [servers, setServers] = useState<Server[]>([]);
  const [form, setForm] = useState(EMPTY);
  const [editId, setEditId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const load = () => api.get("/servers/").then((r) => setServers(r.data));

  useEffect(() => {
    load();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (editId) {
        await api.put(`/servers/${editId}`, form);
      } else {
        await api.post("/servers/", form);
      }
      setForm(EMPTY);
      setEditId(null);
      load();
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        setError(axiosErr.response?.data?.detail || "Failed");
      } else {
        setError("Failed");
      }
    }
  };

  const startEdit = (s: Server) => {
    setEditId(s.id);
    setForm({
      hostname: s.hostname,
      ip_address: s.ip_address,
      os: s.os || "",
      environment: s.environment || "",
      status: s.status,
      description: s.description || "",
    });
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this server?")) return;
    await api.delete(`/servers/${id}`);
    load();
  };

  return (
    <div>
      <h1 style={{ margin: "20px 0" }}>Server Inventory</h1>

      <div className="card">
        <h2>{editId ? "Edit Server" : "Add Server"}</h2>
        {error && <p className="error-msg">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div className="form-group">
              <label>Hostname</label>
              <input value={form.hostname} onChange={(e) => setForm({ ...form, hostname: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>IP Address</label>
              <input value={form.ip_address} onChange={(e) => setForm({ ...form, ip_address: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>OS</label>
              <input value={form.os || ""} onChange={(e) => setForm({ ...form, os: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Environment</label>
              <input value={form.environment || ""} onChange={(e) => setForm({ ...form, environment: e.target.value })} placeholder="production, staging, dev" />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="maintenance">Maintenance</option>
              </select>
            </div>
            <div className="form-group">
              <label>Description</label>
              <input value={form.description || ""} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">
            {editId ? "Update" : "Add Server"}
          </button>
          {editId && (
            <button
              type="button"
              className="btn"
              style={{ marginLeft: 8 }}
              onClick={() => {
                setEditId(null);
                setForm(EMPTY);
              }}
            >
              Cancel
            </button>
          )}
        </form>
      </div>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Hostname</th>
              <th>IP</th>
              <th>OS</th>
              <th>Environment</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {servers.map((s) => (
              <tr key={s.id}>
                <td>{s.hostname}</td>
                <td>{s.ip_address}</td>
                <td>{s.os || "—"}</td>
                <td>{s.environment || "—"}</td>
                <td>
                  <span className={`status-badge status-${s.status}`}>{s.status}</span>
                </td>
                <td>
                  <button className="btn btn-primary" style={{ marginRight: 4, padding: "4px 12px" }} onClick={() => startEdit(s)}>
                    Edit
                  </button>
                  <button className="btn btn-danger" style={{ padding: "4px 12px" }} onClick={() => handleDelete(s.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
            {servers.length === 0 && (
              <tr>
                <td colSpan={6}>No servers found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
