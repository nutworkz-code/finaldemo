# OpsInsight Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Browser                        │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTPS
┌───────────────────────────▼──────────────────────────────────┐
│                    Nginx / Ingress Controller                │
│                   (Reverse Proxy + Static Files)             │
└──────┬───────────────────────────────────────┬───────────────┘
       │ /api/*                                │ /*
┌──────▼──────────────┐              ┌─────────▼──────────────┐
│   FastAPI Backend   │              │   React Frontend       │
│   (Python 3.12)     │              │   (Vite + TypeScript)  │
│                     │              │                        │
│  ┌───────────────┐  │              │  ┌──────────────────┐  │
│  │ Auth (JWT)    │  │              │  │ Dashboard Page   │  │
│  │ Server CRUD   │  │              │  │ Servers Page     │  │
│  │ K8s Status    │  │              │  │ Kubernetes Page  │  │
│  │ CSV Upload    │  │              │  │ CSV Upload Page  │  │
│  │ Dashboard API │  │              │  │ Login Page       │  │
│  │ Audit Logging │  │              │  └──────────────────┘  │
│  └───────┬───────┘  │              │                        │
└──────────┼──────────┘              └────────────────────────┘
           │ SQLAlchemy ORM
┌──────────▼──────────┐
│   PostgreSQL 16     │
│   (Data Store)      │
│                     │
│  Tables:            │
│  - users            │
│  - servers          │
│  - audit_logs       │
└─────────────────────┘
```

## Component Details

### Backend (FastAPI)
- **Authentication**: JWT-based with bcrypt password hashing
- **API Documentation**: Auto-generated Swagger UI at `/api/docs`
- **Audit Middleware**: Intercepts POST/PUT/PATCH/DELETE requests and logs them
- **Database**: SQLAlchemy ORM with PostgreSQL
- **CSV Parser**: Parses uploaded CSV files and bulk-imports server records

### Frontend (React + TypeScript)
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios with token interceptor
- **Pages**: Login, Dashboard, Servers (CRUD), Kubernetes, CSV Upload

### Infrastructure
- **Local Dev**: Docker Compose (PostgreSQL + Backend + Frontend)
- **Kubernetes**: Raw manifests in `k8s/`
- **Production**: Helm chart in `helm/opsinsight/`
- **CI/CD**: GitHub Actions (lint, test, build images)

## Design Decisions

1. **JWT Authentication** — Stateless, scalable, no session store needed
2. **SQLAlchemy ORM** — Type-safe database access with migration support
3. **Audit Middleware** — Decoupled logging without touching business logic
4. **Mock K8s Data** — Allows frontend development without a real cluster
5. **Vite** — Fast build tool with HMR for React development
6. **Multi-stage Docker** — Smaller production images
7. **Helm Chart** — Parameterized deployments for different environments
