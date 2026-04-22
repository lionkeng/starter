"""
A small collection of utility functions used across our backend services.

Each function has known issues reported by users or observed in production.
Your job: find the bug, fix it, and write a one-sentence explanation of
what was actually wrong in the comment above each function.

Do not change function signatures. The existing tests must still pass,
and your fixes should not introduce regressions.
"""

from datetime import datetime, timedelta


# BUG EXPLANATION (fill in):
def paginate(items, page, page_size):
    """
    Return the slice of `items` for the given 1-indexed page.
    Example: paginate([a,b,c,d,e], page=2, page_size=2) -> [c, d]
    """
    start = page * page_size
    end = start + page_size
    return items[start:end]


# BUG EXPLANATION (fill in):
def collect_errors(new_error, errors=[]):
    """
    Append a new error message to the running list of errors and return it.
    Used by our request validator to accumulate issues across checks.
    """
    errors.append(new_error)
    return errors


# BUG EXPLANATION (fill in):
def fetch_user_age(user_record):
    """
    Return the integer age of a user given a record dict with a 'birthdate'
    field in 'YYYY-MM-DD' format. Returns None if the record is malformed.
    """
    try:
        birthdate = datetime.strptime(user_record["birthdate"], "%Y-%m-%d")
        today = datetime.now()
        return today.year - birthdate.year
    except Exception:
        return None


# BUG EXPLANATION (fill in):
def is_session_expired(session_start_iso, ttl_hours=24):
    """
    Given an ISO 8601 timestamp string for when a session started,
    return True if the session has exceeded its TTL.

    Session timestamps come from our API in UTC (e.g. '2026-04-22T10:30:00+00:00').
    """
    session_start = datetime.fromisoformat(session_start_iso)
    now = datetime.now()
    return (now - session_start) > timedelta(hours=ttl_hours)
