def test_list_version_key_format(kb):
    key = kb.list_version_key(entity="user", companies_ids=["company-1"])
    assert key.startswith("test-tenant:test-service:user:list:c:")
    assert key.endswith(":version")


def test_list_version_key_deterministic(kb):
    a = kb.list_version_key(entity="user", companies_ids=["company-1", "company-2"])
    b = kb.list_version_key(entity="user", companies_ids=["company-1", "company-2"])
    assert a == b


def test_list_version_key_order_independent(kb):
    a = kb.list_version_key(entity="user", companies_ids=["company-2", "company-1"])
    b = kb.list_version_key(entity="user", companies_ids=["company-1", "company-2"])
    assert a == b


def test_list_version_key_different_for_different_entities(kb):
    a = kb.list_version_key(entity="user", companies_ids=["company-1"])
    b = kb.list_version_key(entity="order", companies_ids=["company-1"])
    assert a != b


def test_list_version_key_different_for_different_companies(kb):
    a = kb.list_version_key(entity="user", companies_ids=["company-1"])
    b = kb.list_version_key(entity="user", companies_ids=["company-2"])
    assert a != b


def test_list_cursor_key_format(kb):
    key = kb.list_cursor_key(
        entity="user",
        companies_ids=["company-1"],
        version=1,
        filters={"status": "active"},
        sort=[{"field": "name", "direction": "asc"}],
        cursor=None,
        limit=20,
    )
    assert key.startswith("test-tenant:test-service:user:list:c:")
    assert ":v1:" in key
    assert ":start:" in key
    assert key.endswith(":20")


def test_list_cursor_key_deterministic(kb):
    params = {
        "entity": "user",
        "companies_ids": ["company-1"],
        "version": 1,
        "filters": {"status": "active"},
        "sort": [],
        "cursor": {"id": "abc"},
        "limit": 10,
    }
    a = kb.list_cursor_key(**params)
    b = kb.list_cursor_key(**params)
    assert a == b


def test_list_cursor_key_with_cursor(kb):
    key = kb.list_cursor_key(
        entity="user",
        companies_ids=["company-1"],
        version=1,
        filters={},
        sort=[],
        cursor={"id": "last-id", "created_at": "2024-01-01T00:00:00Z"},
        limit=20,
    )
    assert ":start:" not in key


def test_list_cursor_key_different_for_different_versions(kb):
    params = {
        "entity": "user",
        "companies_ids": ["company-1"],
        "filters": {},
        "sort": [],
        "cursor": None,
        "limit": 10,
    }
    a = kb.list_cursor_key(version=1, **params)
    b = kb.list_cursor_key(version=2, **params)
    assert a != b


def test_list_cursor_key_different_for_different_limits(kb):
    params = {
        "entity": "user",
        "companies_ids": ["company-1"],
        "version": 1,
        "filters": {},
        "sort": [],
        "cursor": None,
    }
    a = kb.list_cursor_key(limit=10, **params)
    b = kb.list_cursor_key(limit=20, **params)
    assert a != b


def test_list_cursor_key_different_for_different_filters(kb):
    params = {
        "entity": "user",
        "companies_ids": ["company-1"],
        "version": 1,
        "sort": [],
        "cursor": None,
        "limit": 10,
    }
    a = kb.list_cursor_key(filters={"status": "active"}, **params)
    b = kb.list_cursor_key(filters={"status": "inactive"}, **params)
    assert a != b


def test_list_cursor_key_companies_order_independent(kb):
    params = {
        "entity": "user",
        "version": 1,
        "filters": {},
        "sort": [],
        "cursor": None,
        "limit": 10,
    }
    a = kb.list_cursor_key(companies_ids=["company-2", "company-1"], **params)
    b = kb.list_cursor_key(companies_ids=["company-1", "company-2"], **params)
    assert a == b
