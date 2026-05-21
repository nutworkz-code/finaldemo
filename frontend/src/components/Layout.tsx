import { Link, Outlet, useNavigate } from "react-router-dom";

export default function Layout() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <>
      <nav className="navbar">
        <span className="brand">OpsInsight</span>
        <Link to="/">Dashboard</Link>
        <Link to="/servers">Servers</Link>
        <Link to="/kubernetes">Kubernetes</Link>
        <Link to="/csv-upload">CSV Upload</Link>
        <a
          href="/api/docs"
          target="_blank"
          rel="noopener noreferrer"
        >
          API Docs
        </a>
        <button className="btn btn-danger" onClick={logout} style={{ marginLeft: "auto" }}>
          Logout
        </button>
      </nav>
      <div className="container">
        <Outlet />
      </div>
    </>
  );
}
