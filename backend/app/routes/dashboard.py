import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit import AuditLog
from app.models.server import Server
from app.models.user import User
from app.schemas.audit import AuditLogResponse
from app.services.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> dict:
    """Get dashboard statistics."""
    total_servers = db.query(Server).count()
    active_servers = db.query(Server).filter(Server.status == "active").count()
    inactive_servers = total_servers - active_servers

    env_counts: dict[str, int] = {}
    servers = db.query(Server).all()
    for s in servers:
        env = s.environment or "unknown"
        env_counts[env] = env_counts.get(env, 0) + 1

    return {
        "total_servers": total_servers,
        "active_servers": active_servers,
        "inactive_servers": inactive_servers,
        "servers_by_environment": env_counts,
    }


@router.get("/audit-logs", response_model=list[AuditLogResponse])
def list_audit_logs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[AuditLog]:
    """Get recent audit log entries."""
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
