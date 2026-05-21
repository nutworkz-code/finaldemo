import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.database import SessionLocal
from app.models.audit import AuditLog

logger = logging.getLogger(__name__)

MUTATION_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


async def audit_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)

    if request.method in MUTATION_METHODS and response.status_code < 400:
        username = None
        if hasattr(request.state, "user"):
            username = request.state.user

        db = SessionLocal()
        try:
            log_entry = AuditLog(
                username=username,
                action=request.method,
                resource=str(request.url.path),
                detail=f"{request.method} {request.url.path} -> {response.status_code}",
            )
            db.add(log_entry)
            db.commit()
        except Exception:
            logger.exception("Failed to write audit log")
            db.rollback()
        finally:
            db.close()

    return response
