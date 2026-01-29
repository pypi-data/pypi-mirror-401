import pytest

from biplex_utils_cache_key_builder import CacheKeyBuilder


class TestEdgeCases:
    def test_empty_company_id(self, kb):
        result = kb.company_hash("")
        assert len(result) == 12

    def test_empty_companies_list(self, kb):
        result = kb.companies_hash([])
        assert len(result) == 12

    def test_company_id_with_special_characters(self, kb):
        result = kb.company_hash("company:with:colons")
        assert len(result) == 12

    def test_company_id_with_unicode(self, kb):
        result = kb.company_hash("компания-123")
        assert len(result) == 12

    def test_entity_id_with_special_characters(self, kb):
        key = kb.entity_key(entity="user", company_id="c1", entity_id="id:with:colons")
        assert "id:with:colons" in key

    def test_filters_with_nested_dict(self, kb):
        filters = {"user": {"name": "test", "age": {"min": 18, "max": 65}}}
        result = kb.query_hash(filters=filters, sort=[])
        assert len(result) == 10

    def test_filters_with_list_values(self, kb):
        filters = {"status": ["active", "pending"]}
        result = kb.query_hash(filters=filters, sort=[])
        assert len(result) == 10

    def test_sort_with_multiple_items(self, kb):
        sort = [
            {"field": "created_at", "direction": "desc"},
            {"field": "name", "direction": "asc"},
        ]
        result = kb.query_hash(filters={}, sort=sort)
        assert len(result) == 10

    def test_cursor_with_only_id(self, kb):
        result = kb.cursor_hash({"id": "abc123"})
        assert len(result) == 8

    def test_cursor_with_only_created_at(self, kb):
        result = kb.cursor_hash({"created_at": "2024-01-01T00:00:00Z"})
        assert len(result) == 8

    def test_large_limit_value(self, kb):
        key = kb.list_cursor_key(
            entity="user",
            companies_ids=["c1"],
            version=1,
            filters={},
            sort=[],
            cursor=None,
            limit=999999,
        )
        assert key.endswith(":999999")

    def test_large_version_number(self, kb):
        key = kb.list_cursor_key(
            entity="user",
            companies_ids=["c1"],
            version=999999,
            filters={},
            sort=[],
            cursor=None,
            limit=10,
        )
        assert ":v999999:" in key

    def test_many_companies(self, kb):
        companies = [f"company-{i}" for i in range(100)]
        result = kb.companies_hash(companies)
        assert len(result) == 12

    def test_different_tenant_and_service(self):
        kb1 = CacheKeyBuilder(tenant="tenant1", service="service1")
        kb2 = CacheKeyBuilder(tenant="tenant2", service="service2")
        key1 = kb1.entity_key(entity="user", company_id="c1", entity_id="123")
        key2 = kb2.entity_key(entity="user", company_id="c1", entity_id="123")
        assert key1 != key2
        assert key1.startswith("tenant1:service1:")
        assert key2.startswith("tenant2:service2:")


class TestHashConsistency:
    def test_sha1_produces_hex_characters(self, kb):
        result = kb.company_hash("test")
        assert all(c in "0123456789abcdef" for c in result)

    def test_query_hash_same_for_semantically_equal_dicts(self, kb):
        a = kb.query_hash(filters={"x": 1, "y": 2}, sort=[])
        b = kb.query_hash(filters={"y": 2, "x": 1}, sort=[])
        assert a == b

    def test_cursor_hash_same_for_semantically_equal_dicts(self, kb):
        a = kb.cursor_hash({"a": 1, "b": 2})
        b = kb.cursor_hash({"b": 2, "a": 1})
        assert a == b
