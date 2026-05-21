import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.server import Server
from app.models.user import User
from app.schemas.server import ServerCreate, ServerResponse, ServerUpdate
from app.services.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/servers", tags=["Server Inventory"])


@router.get("/", response_model=list[ServerResponse])
def list_servers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> list[Server]:
    """List all servers with pagination."""
    return db.query(Server).offset(skip).limit(limit).all()


@router.get("/{server_id}", response_model=ServerResponse)
def get_server(
    server_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Server:
    """Get a single server by ID."""
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.post("/", response_model=ServerResponse, status_code=status.HTTP_201_CREATED)
def create_server(
    server_in: ServerCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Server:
    """Create a new server entry."""
    existing = db.query(Server).filter(Server.hostname == server_in.hostname).first()
    if existing:
        raise HTTPException(status_code=400, detail="Hostname already exists")

    server = Server(**server_in.model_dump())
    db.add(server)
    db.commit()
    db.refresh(server)
    logger.info("Server created: %s", server.hostname)
    return server


@router.put("/{server_id}", response_model=ServerResponse)
def update_server(
    server_id: int,
    server_in: ServerUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Server:
    """Update an existing server."""
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    update_data = server_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)
    logger.info("Server updated: %s", server.hostname)
    return server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_server(
    server_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> None:
    """Delete a server."""
    server = db.query(Server).filter(Server.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    db.delete(server)
    db.commit()
    logger.info("Server deleted: id=%d", server_id)
