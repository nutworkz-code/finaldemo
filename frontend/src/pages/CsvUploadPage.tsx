import { useState } from "react";
import api from "../services/api";

interface UploadResult {
  filename: string;
  created: number;
  skipped: number;
  errors: string[];
}

export default function CsvUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setError("");
    setResult(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await api.post("/csv/upload", formData);
      setResult(resp.data);
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        setError(axiosErr.response?.data?.detail || "Upload failed");
      } else {
        setError("Upload failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 style={{ margin: "20px 0" }}>CSV Upload</h1>

      <div className="card">
        <h2>Upload Server Inventory CSV</h2>
        <p style={{ marginBottom: 16, color: "#6b7280" }}>
          CSV must contain columns: <strong>hostname</strong>, <strong>ip_address</strong>.
          Optional: os, environment, status, description.
        </p>
        {error && <p className="error-msg">{error}</p>}
        <form onSubmit={handleUpload}>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <button type="submit" className="btn btn-primary" disabled={!file || loading}>
            {loading ? "Uploading..." : "Upload"}
          </button>
        </form>
      </div>

      {result && (
        <div className="card success-msg">
          <h3>Upload Complete: {result.filename}</h3>
          <p>Created: {result.created} | Skipped: {result.skipped}</p>
          {result.errors.length > 0 && (
            <ul style={{ marginTop: 8, paddingLeft: 20 }}>
              {result.errors.map((e, i) => (
                <li key={i} style={{ color: "#856404" }}>
                  {e}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="card">
        <h2>CSV Template</h2>
        <pre style={{ background: "#f1f3f5", padding: 16, borderRadius: 6, overflow: "auto" }}>
{`hostname,ip_address,os,environment,status,description
web-01,10.0.1.1,Ubuntu 22.04,production,active,Main web server
db-01,10.0.2.1,CentOS 9,production,active,Primary database
staging-01,10.0.3.1,Ubuntu 22.04,staging,active,Staging server`}
        </pre>
      </div>
    </div>
  );
}
