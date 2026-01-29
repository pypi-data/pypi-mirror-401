def test_entity_key_format(kb):
    key = kb.entity_key(entity="user", company_id="company-1", entity_id="user-123")
    assert key.startswith("test-tenant:test-service:user:item:c:")
    assert key.endswith(":user-123")


def test_entity_key_contains_company_hash(kb):
    key = kb.entity_key(entity="user", company_id="company-1", entity_id="user-123")
    parts = key.split(":")
    company_hash_part = parts[5]
    assert len(company_hash_part) == 12


def test_entity_key_deterministic(kb):
    a = kb.entity_key(entity="user", company_id="company-1", entity_id="user-123")
    b = kb.entity_key(entity="user", company_id="company-1", entity_id="user-123")
    assert a == b


def test_entity_key_different_for_different_entities(kb):
    a = kb.entity_key(entity="user", company_id="company-1", entity_id="123")
    b = kb.entity_key(entity="order", company_id="company-1", entity_id="123")
    assert a != b


def test_entity_key_different_for_different_companies(kb):
    a = kb.entity_key(entity="user", company_id="company-1", entity_id="123")
    b = kb.entity_key(entity="user", company_id="company-2", entity_id="123")
    assert a != b


def test_entity_key_different_for_different_entity_ids(kb):
    a = kb.entity_key(entity="user", company_id="company-1", entity_id="123")
    b = kb.entity_key(entity="user", company_id="company-1", entity_id="456")
    assert a != b


def test_entity_key_uses_tenant_and_service(kb):
    key = kb.entity_key(entity="user", company_id="company-1", entity_id="123")
    assert key.startswith("test-tenant:test-service:")
