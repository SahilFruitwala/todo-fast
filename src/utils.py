from datetime import datetime, timezone


def utc_time():
    return datetime.now(timezone.utc)
