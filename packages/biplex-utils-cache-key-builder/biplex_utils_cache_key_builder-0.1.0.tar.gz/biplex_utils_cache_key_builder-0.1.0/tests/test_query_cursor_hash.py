def test_query_hash_returns_10_chars(kb):
    result = kb.query_hash(filters={"status": "active"}, sort=[{"field": "name", "direction": "asc"}])
    assert len(result) == 10


def test_query_hash_deterministic(kb):
    a = kb.query_hash(filters={"status": "active"}, sort=[])
    b = kb.query_hash(filters={"status": "active"}, sort=[])
    assert a == b


def test_query_hash_order_independent_for_filters(kb):
    a = kb.query_hash(filters={"a": 1, "b": 2}, sort=[])
    b = kb.query_hash(filters={"b": 2, "a": 1}, sort=[])
    assert a == b


def test_query_hash_different_for_different_filters(kb):
    a = kb.query_hash(filters={"status": "active"}, sort=[])
    b = kb.query_hash(filters={"status": "inactive"}, sort=[])
    assert a != b


def test_query_hash_different_for_different_sort(kb):
    a = kb.query_hash(filters={}, sort=[{"field": "name", "direction": "asc"}])
    b = kb.query_hash(filters={}, sort=[{"field": "name", "direction": "desc"}])
    assert a != b


def test_query_hash_empty_filters_and_sort(kb):
    result = kb.query_hash(filters={}, sort=[])
    assert len(result) == 10


def test_query_hash_none_filters_and_sort(kb):
    result = kb.query_hash(filters=None, sort=None)
    assert len(result) == 10


def test_cursor_hash_returns_start_for_none(kb):
    assert kb.cursor_hash(None) == "start"


def test_cursor_hash_returns_start_for_empty_dict(kb):
    assert kb.cursor_hash({}) == "start"


def test_cursor_hash_returns_8_chars(kb):
    result = kb.cursor_hash({"id": "abc123", "created_at": "2024-01-01T00:00:00Z"})
    assert len(result) == 8


def test_cursor_hash_deterministic(kb):
    cursor = {"id": "abc123", "created_at": "2024-01-01T00:00:00Z"}
    a = kb.cursor_hash(cursor)
    b = kb.cursor_hash(cursor)
    assert a == b


def test_cursor_hash_order_independent(kb):
    a = kb.cursor_hash({"id": "abc", "created_at": "2024-01-01"})
    b = kb.cursor_hash({"created_at": "2024-01-01", "id": "abc"})
    assert a == b


def test_cursor_hash_different_for_different_cursors(kb):
    a = kb.cursor_hash({"id": "abc"})
    b = kb.cursor_hash({"id": "xyz"})
    assert a != b
