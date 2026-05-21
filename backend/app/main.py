import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.middleware.audit import audit_middleware
from app.routes import auth, csv_upload, dashboard, kubernetes, servers

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("OpsInsight API started — tables created")
    yield


app = FastAPI(
    title="OpsInsight API",
    description="Internal operations platform for infrastructure management",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(audit_middleware)

app.include_router(auth.router)
app.include_router(servers.router)
app.include_router(kubernetes.router)
app.include_router(csv_upload.router)
app.include_router(dashboard.router)


@app.get("/api/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "healthy", "service": "opsinsight-api"}
