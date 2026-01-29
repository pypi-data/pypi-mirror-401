def test_company_hash_returns_12_chars(kb):
    result = kb.company_hash("company-123")
    assert len(result) == 12


def test_company_hash_deterministic(kb):
    a = kb.company_hash("company-123")
    b = kb.company_hash("company-123")
    assert a == b


def test_company_hash_different_for_different_ids(kb):
    a = kb.company_hash("company-1")
    b = kb.company_hash("company-2")
    assert a != b


def test_companies_hash_returns_12_chars(kb):
    result = kb.companies_hash(["company-1", "company-2"])
    assert len(result) == 12


def test_companies_hash_deterministic(kb):
    a = kb.companies_hash(["company-1", "company-2"])
    b = kb.companies_hash(["company-1", "company-2"])
    assert a == b


def test_companies_hash_deduplicates(kb):
    a = kb.companies_hash(["company-1", "company-1", "company-2"])
    b = kb.companies_hash(["company-1", "company-2"])
    assert a == b


def test_companies_hash_single_company(kb):
    result = kb.companies_hash(["company-1"])
    assert len(result) == 12


def test_companies_hash_from_generator(kb):
    def gen():
        yield "company-1"
        yield "company-2"

    result = kb.companies_hash(gen())
    assert len(result) == 12
