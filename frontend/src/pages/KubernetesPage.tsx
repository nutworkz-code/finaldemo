import { useEffect, useState } from "react";
import api from "../services/api";

interface Node {
  name: string;
  status: string;
  roles: string;
  cpu_usage_percent: number;
  memory_usage_percent: number;
  pods_running: number;
}

interface Pod {
  name: string;
  namespace: string;
  status: string;
  restarts: number;
  age_hours: number;
}

interface ClusterStatus {
  cluster_name: string;
  version: string;
  nodes: Node[];
  total_pods: number;
  pods: Pod[];
  namespaces: number;
}

export default function KubernetesPage() {
  const [cluster, setCluster] = useState<ClusterStatus | null>(null);

  useEffect(() => {
    api.get("/kubernetes/status").then((r) => setCluster(r.data));
  }, []);

  if (!cluster) return <p>Loading...</p>;

  return (
    <div>
      <h1 style={{ margin: "20px 0" }}>Kubernetes Cluster</h1>

      <div className="stat-grid">
        <div className="stat-card">
          <h3>{cluster.cluster_name}</h3>
          <p>Cluster</p>
        </div>
        <div className="stat-card">
          <h3>{cluster.version}</h3>
          <p>Version</p>
        </div>
        <div className="stat-card">
          <h3>{cluster.nodes.length}</h3>
          <p>Nodes</p>
        </div>
        <div className="stat-card">
          <h3>{cluster.total_pods}</h3>
          <p>Total Pods</p>
        </div>
      </div>

      <div className="card">
        <h2>Nodes</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Role</th>
              <th>Status</th>
              <th>CPU %</th>
              <th>Memory %</th>
              <th>Pods</th>
            </tr>
          </thead>
          <tbody>
            {cluster.nodes.map((n) => (
              <tr key={n.name}>
                <td>{n.name}</td>
                <td>{n.roles}</td>
                <td>
                  <span className={`status-badge status-${n.status}`}>{n.status}</span>
                </td>
                <td>{n.cpu_usage_percent}%</td>
                <td>{n.memory_usage_percent}%</td>
                <td>{n.pods_running}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Pods</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Namespace</th>
              <th>Status</th>
              <th>Restarts</th>
              <th>Age (hrs)</th>
            </tr>
          </thead>
          <tbody>
            {cluster.pods.map((p) => (
              <tr key={p.name}>
                <td>{p.name}</td>
                <td>{p.namespace}</td>
                <td>
                  <span className={`status-badge status-${p.status}`}>{p.status}</span>
                </td>
                <td>{p.restarts}</td>
                <td>{p.age_hours}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
