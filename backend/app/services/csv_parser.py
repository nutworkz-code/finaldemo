import csv
import io
import logging

from sqlalchemy.orm import Session

from app.models.server import Server

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"hostname", "ip_address"}
OPTIONAL_COLUMNS = {"os", "environment", "status", "description"}
ALL_COLUMNS = REQUIRED_COLUMNS | OPTIONAL_COLUMNS


def parse_csv(file_content: bytes, db: Session) -> dict:
    text = file_content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV file is empty or has no headers")

    headers = set(reader.fieldnames)
    missing = REQUIRED_COLUMNS - headers
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    created = 0
    skipped = 0
    errors: list[str] = []

    for i, row in enumerate(reader, start=2):
        hostname = row.get("hostname", "").strip()
        ip_address = row.get("ip_address", "").strip()

        if not hostname or not ip_address:
            errors.append(f"Row {i}: missing hostname or ip_address")
            skipped += 1
            continue

        existing = db.query(Server).filter(Server.hostname == hostname).first()
        if existing:
            skipped += 1
            continue

        server = Server(
            hostname=hostname,
            ip_address=ip_address,
            os=row.get("os", "").strip() or None,
            environment=row.get("environment", "").strip() or None,
            status=row.get("status", "active").strip() or "active",
            description=row.get("description", "").strip() or None,
        )
        db.add(server)
        created += 1

    db.commit()
    logger.info("CSV import: created=%d skipped=%d errors=%d", created, skipped, len(errors))
    return {"created": created, "skipped": skipped, "errors": errors}
