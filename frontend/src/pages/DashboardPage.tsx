import { useEffect, useState } from "react";
import api from "../services/api";

interface DashboardStats {
  total_servers: number;
  active_servers: number;
  inactive_servers: number;
  servers_by_environment: Record<string, number>;
}

interface AuditEntry {
  id: number;
  username: string | null;
  action: string;
  resource: string;
  detail: string | null;
  timestamp: string;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [logs, setLogs] = useState<AuditEntry[]>([]);

  useEffect(() => {
    api.get("/dashboard/stats").then((r) => setStats(r.data));
    api.get("/dashboard/audit-logs?limit=10").then((r) => setLogs(r.data));
  }, []);

  if (!stats) return <p>Loading...</p>;

  return (
    <div>
      <h1 style={{ margin: "20px 0" }}>Dashboard</h1>
      <div className="stat-grid">
        <div className="stat-card">
          <h3>{stats.total_servers}</h3>
          <p>Total Servers</p>
        </div>
        <div className="stat-card">
          <h3>{stats.active_servers}</h3>
          <p>Active</p>
        </div>
        <div className="stat-card">
          <h3>{stats.inactive_servers}</h3>
          <p>Inactive</p>
        </div>
      </div>

      <div className="card">
        <h2>Servers by Environment</h2>
        <table>
          <thead>
            <tr>
              <th>Environment</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(stats.servers_by_environment).map(([env, count]) => (
              <tr key={env}>
                <td>{env}</td>
                <td>{count}</td>
              </tr>
            ))}
            {Object.keys(stats.servers_by_environment).length === 0 && (
              <tr>
                <td colSpan={2}>No servers yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Recent Audit Logs</h2>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>User</th>
              <th>Action</th>
              <th>Resource</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id}>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>{log.username || "—"}</td>
                <td>{log.action}</td>
                <td>{log.resource}</td>
              </tr>
            ))}
            {logs.length === 0 && (
              <tr>
                <td colSpan={4}>No audit logs yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
