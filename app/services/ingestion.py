from pathlib import Path
from datetime import datetime
import hashlib

import pandas as pd
from django.db import transaction

from app.models import FileIngestion, RawAdsRow

def compute_file_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

def parse_filename(file_path: Path) -> tuple:
    """
    Extract extraction_date and attribution_window from filename.

    Example:
    2022-06-01_day7_anon.csv
    ->
    extraction_date = 2022-06-01
    attribution_window = day7
    """

    filename = file_path.name
    parts = filename.split("_")

    extraction_date = datetime.strptime(parts[0], "%Y-%m-%d").date()
    attribution_window = parts[1]

    return extraction_date, attribution_window


@transaction.atomic
def ingest_file(file_path: str) -> dict:
    """
    Ingest a CSV into the raw layer.

    Atomic transaction:
    either the entire file is ingested successfully or no data is persisted.

    Idempotency:
    if the exact same file content was already ingested, the ingestion is skipped.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_hash = compute_file_hash(file_path)

    existing_ingestion = FileIngestion.objects.filter(
        file_hash=file_hash
    ).first()

    if existing_ingestion:
        return {
            "status": "skipped",
            "reason": "file_already_ingested",
            "filename": existing_ingestion.filename,
            "row_count": existing_ingestion.row_count,
        }

    extraction_date, attribution_window = parse_filename(file_path)

    df = pd.read_csv(file_path)

    ingestion = FileIngestion.objects.create(
        filename=file_path.name,
        file_hash=file_hash,
        extraction_date=extraction_date,
        attribution_window=attribution_window,
        row_count=len(df),
    )

    raw_rows = []

    for index, row in df.iterrows():
        raw_rows.append(
            RawAdsRow(
                ingestion=ingestion,
                date=row["date"],
                platform=row["platform"],
                country_x_language=row["country_x_language"],
                campaign_id=row["campaign_id"],
                ad_id=row["ad_id"],
                spend=row["spend"],
                installs=row["installs"],
            )
        )

    RawAdsRow.objects.bulk_create(raw_rows)

    return {
        "status": "ingested",
        "filename": file_path.name,
        "row_count": len(raw_rows),
        "extraction_date": extraction_date,
        "attribution_window": attribution_window,
    }


def ingest_directory(directory_path: str) -> dict:
    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")

    results = []

    for file_path in sorted(directory_path.glob("*.csv")):
        result = ingest_file(str(file_path))
        results.append(result)

    return {
        "status": "completed",
        "directory": str(directory_path),
        "files_count": len(results),
        "ingested_count": sum(1 for r in results if r["status"] == "ingested"),
        "skipped_count": sum(1 for r in results if r["status"] == "skipped"),
        "results": results,
    }