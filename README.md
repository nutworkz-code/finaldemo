# OpsInsight

Internal web application for infrastructure management, server inventory tracking, and Kubernetes cluster monitoring.

## Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Frontend       | React 18, TypeScript, Vite          |
| Backend        | Python 3.12, FastAPI                |
| Database       | PostgreSQL 16                       |
| Auth           | JWT (python-jose + passlib/bcrypt)  |
| Infrastructure | Docker, Kubernetes, Helm            |
| CI/CD          | GitHub Actions                      |

## Features

- **Dashboard** — Server statistics and recent audit logs
- **Server Inventory** — Full CRUD for managing servers
- **Kubernetes Status** — Cluster node and pod overview
- **CSV Upload** — Bulk-import server records from CSV files
- **REST API Docs** — Interactive Swagger UI at `/api/docs`
- **Audit Logging** — Automatic logging of all mutations

## Quick Start (Docker Compose)

```bash
# Clone the repository
git clone https://github.com/nutworkz-code/finaldemo.git
cd finaldemo

# Start all services
docker compose up --build -d

# Access the application
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/api/docs
```

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest httpx ruff

# Start PostgreSQL (or use Docker)
docker run -d --name pg -e POSTGRES_USER=opsinsight -e POSTGRES_PASSWORD=opsinsight -e POSTGRES_DB=opsinsight -p 5432:5432 postgres:16-alpine

# Run the backend
uvicorn app.main:app --reload

# Run tests
pytest -v

# Lint
ruff check .
ruff format --check .
```

### Frontend

```bash
cd frontend
npm install

# Start dev server (proxies /api to backend)
npm run dev

# Lint
npm run lint

# Build
npm run build
```

## Kubernetes Deployment

### Raw Manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/ingress.yaml
```

### Helm Chart

```bash
helm install opsinsight ./helm/opsinsight --namespace opsinsight --create-namespace

# Custom values
helm install opsinsight ./helm/opsinsight \
  --set backend.replicas=3 \
  --set ingress.host=ops.example.com
```

## API Endpoints

| Method | Path                       | Description                |
|--------|----------------------------|----------------------------|
| POST   | `/api/auth/register`       | Register a new user        |
| POST   | `/api/auth/login`          | Login and get JWT token    |
| GET    | `/api/auth/me`             | Get current user info      |
| GET    | `/api/servers/`            | List all servers           |
| POST   | `/api/servers/`            | Create a server            |
| GET    | `/api/servers/{id}`        | Get server by ID           |
| PUT    | `/api/servers/{id}`        | Update a server            |
| DELETE | `/api/servers/{id}`        | Delete a server            |
| POST   | `/api/csv/upload`          | Upload CSV inventory file  |
| GET    | `/api/kubernetes/status`   | Get K8s cluster status     |
| GET    | `/api/dashboard/stats`     | Get dashboard statistics   |
| GET    | `/api/dashboard/audit-logs`| Get recent audit logs      |
| GET    | `/api/health`              | Health check               |

## Project Structure

```
finaldemo/
├── .github/workflows/ci.yml     # CI pipeline
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # ORM models
│   │   ├── routes/              # API endpoints
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── middleware/          # Audit middleware
│   ├── tests/                   # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # React pages
│   │   ├── components/          # Shared components
│   │   └── services/            # API client
│   ├── Dockerfile
│   └── package.json
├── k8s/                         # Kubernetes manifests
├── helm/opsinsight/             # Helm chart
├── docker-compose.yml           # Local deployment
└── docs/architecture.md         # Architecture diagram
```

## Testing

```bash
cd backend
pytest -v
```

Runs 14+ unit tests covering authentication, server CRUD, CSV upload, dashboard, and health endpoints.

## CI Pipeline

The GitHub Actions pipeline runs on every push and PR to `main`:

1. **Backend Lint** — Ruff linter and formatter check
2. **Backend Tests** — pytest with SQLite in-memory database
3. **Frontend Lint** — ESLint with TypeScript rules
4. **Frontend Build** — TypeScript check + Vite production build
5. **Docker Build** — Builds both container images
