import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth import get_current_user
from app.services.csv_parser import parse_csv

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/csv", tags=["CSV Upload"])


@router.post("/upload")
async def upload_csv(
    file: UploadFile,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> dict:
    """Upload a CSV file to bulk-import server inventory."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    try:
        result = parse_csv(content, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("CSV upload failed")
        raise HTTPException(status_code=500, detail="Failed to process CSV file")

    logger.info("CSV uploaded: %s", file.filename)
    return {"filename": file.filename, **result}
