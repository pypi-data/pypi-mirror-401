import json
from typing import Iterable


def canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def normalize_companies(companies_ids: Iterable[str]) -> str:
    normalized = sorted(set(companies_ids))
    return ",".join(normalized)
