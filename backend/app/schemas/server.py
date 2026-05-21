from datetime import datetime

from pydantic import BaseModel


class ServerCreate(BaseModel):
    hostname: str
    ip_address: str
    os: str | None = None
    environment: str | None = None
    status: str = "active"
    description: str | None = None


class ServerUpdate(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    os: str | None = None
    environment: str | None = None
    status: str | None = None
    description: str | None = None


class ServerResponse(BaseModel):
    id: int
    hostname: str
    ip_address: str
    os: str | None
    environment: str | None
    status: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
