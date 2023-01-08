from datetime import datetime, timedelta, timezone
from pathlib import Path

from news import CACHE_DIR, LAST_EXTRACTION_FILE
from utility import iso


def check_jobs() -> list[str]:
    errors = []

    last_extraction_path = Path(CACHE_DIR) / LAST_EXTRACTION_FILE
    if last_extraction_path.is_file():
        mtime = datetime.fromtimestamp(
            last_extraction_path.stat().st_mtime, timezone.utc
        )

        now = datetime.now(timezone.utc)
        age = now - mtime

        extractor_period = timedelta(minutes=5)
        jitter = timedelta(seconds=30)
        max_age = extractor_period + jitter

        if age > max_age:
            minutes = age // timedelta(minutes=1)
            errors.append(
                f'Extractor last ran on {iso(mtime)} ({minutes} minutes ago)'
            )
    else:
        errors.append(f'{last_extraction_path} is missing')

    return errors
