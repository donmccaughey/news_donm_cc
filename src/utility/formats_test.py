from datetime import datetime
from .formats import iso, utc


def test_iso():
    dt = datetime.fromisoformat('2023-01-07T20:28:34.989964+00:00')

    assert iso(dt) == '2023-01-07T20:28:34+00:00'


def test_utc():
    dt = datetime.fromisoformat('2023-01-07T20:28:34.989964+00:00')

    assert utc(dt) == '2023-01-07 20:28:34 UTC'


def test_utc_from_other_tz():
    dt = datetime.fromisoformat('2023-01-07T20:28:34.989964-08:00')

    assert utc(dt) == '2023-01-08 04:28:34 UTC'
