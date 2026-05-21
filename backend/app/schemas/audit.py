from datetime import datetime

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    username: str | None
    action: str
    resource: str
    detail: str | None
    timestamp: datetime

    model_config = {"from_attributes": True}
