from datetime import datetime, timezone


def iso(value: datetime) -> str:
    return datetime.isoformat(value, timespec='seconds')


def utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
