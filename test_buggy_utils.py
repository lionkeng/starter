"""
Run with: python -m pytest test_buggy_utils.py -v
Or without pytest: python test_buggy_utils.py
"""

from datetime import datetime, timezone, timedelta
from buggy_utils import paginate, collect_errors, fetch_user_age, is_session_expired


# ---- paginate ----

def test_paginate_first_page():
    # Pages are 1-indexed: page 1 returns the first slice.
    assert paginate(["a", "b", "c", "d", "e"], page=1, page_size=2) == ["a", "b"]


def test_paginate_second_page():
    assert paginate(["a", "b", "c", "d", "e"], page=2, page_size=2) == ["c", "d"]


def test_paginate_last_partial_page():
    assert paginate(["a", "b", "c", "d", "e"], page=3, page_size=2) == ["e"]


# ---- collect_errors ----

def test_collect_errors_single_call():
    result = collect_errors("missing email", errors=[])
    assert result == ["missing email"]


# ---- fetch_user_age ----

def test_fetch_user_age_basic():
    # This test is written to pass even when the bug is present,
    # because it uses a birthday that has already occurred this year.
    record = {"birthdate": "1990-01-01"}
    age = fetch_user_age(record)
    assert age is not None
    assert age > 0


def test_fetch_user_age_malformed():
    assert fetch_user_age({"birthdate": "not-a-date"}) is None
    assert fetch_user_age({}) is None


# ---- is_session_expired ----

def test_is_session_expired_fresh():
    # A session that just started should not be expired.
    # This may or may not pass depending on the machine's local timezone.
    recent = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
    assert is_session_expired(recent) is False


def test_is_session_expired_old():
    old = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    assert is_session_expired(old) is True


if __name__ == "__main__":
    import sys
    tests = [
        test_paginate_first_page,
        test_paginate_second_page,
        test_paginate_last_partial_page,
        test_collect_errors_single_call,
        test_fetch_user_age_basic,
        test_fetch_user_age_malformed,
        test_is_session_expired_fresh,
        test_is_session_expired_old,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
