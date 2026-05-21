import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isRegister, setIsRegister] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (isRegister) {
        await api.post("/auth/register", { username, password });
      }
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      const resp = await api.post("/auth/login", params);
      localStorage.setItem("token", resp.data.access_token);
      navigate("/");
    } catch (err: unknown) {
      if (err && typeof err === "object" && "response" in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        setError(axiosErr.response?.data?.detail || "Authentication failed");
      } else {
        setError("Authentication failed");
      }
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h2>{isRegister ? "Register" : "Login"}</h2>
        {error && <p className="error-msg">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: "100%" }}>
            {isRegister ? "Register & Login" : "Login"}
          </button>
        </form>
        <p style={{ textAlign: "center", marginTop: 16 }}>
          <a href="#" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? "Already have an account? Login" : "Need an account? Register"}
          </a>
        </p>
      </div>
    </div>
  );
}
