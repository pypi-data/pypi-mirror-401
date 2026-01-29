def test_companies_order_independent(kb):
    a = kb.companies_hash(["b", "a"])
    b = kb.companies_hash(["a", "b"])
    assert a == b
