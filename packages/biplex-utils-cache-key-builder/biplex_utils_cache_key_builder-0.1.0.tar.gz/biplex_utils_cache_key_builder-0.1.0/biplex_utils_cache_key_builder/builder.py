from typing import Iterable, Optional

from .hashing import sha1
from .normalize import canonical_json, normalize_companies


class CacheKeyBuilder:
    def __init__(self, tenant: str, service: str):
        self.tenant = tenant
        self.service = service

    # -------- company --------

    def company_hash(self, company_id: str) -> str:
        return sha1(company_id, 12)

    def companies_hash(self, companies_ids: Iterable[str]) -> str:
        return sha1(normalize_companies(companies_ids), 12)

    # -------- query / cursor --------

    def query_hash(self, filters: dict, sort: list) -> str:
        payload = {"filters": filters or {}, "sort": sort or []}
        return sha1(canonical_json(payload), 10)

    def cursor_hash(self, cursor: Optional[dict]) -> str:
        if not cursor:
            return "start"
        return sha1(canonical_json(cursor), 8)

    # -------- keys --------

    def entity_key(
        self,
        entity: str,
        company_id: str,
        entity_id: str,
    ) -> str:
        return (
            f"{self.tenant}:{self.service}:{entity}:item:"
            f"c:{self.company_hash(company_id)}:{entity_id}"
        )

    def list_version_key(
        self,
        entity: str,
        companies_ids: Iterable[str],
    ) -> str:
        return (
            f"{self.tenant}:{self.service}:{entity}:list:"
            f"c:{self.companies_hash(companies_ids)}:version"
        )

    def list_cursor_key(
        self,
        entity: str,
        companies_ids: Iterable[str],
        version: int,
        filters: dict,
        sort: list,
        cursor: Optional[dict],
        limit: int,
    ) -> str:
        return (
            f"{self.tenant}:{self.service}:{entity}:list:"
            f"c:{self.companies_hash(companies_ids)}:"
            f"v{version}:"
            f"{self.query_hash(filters, sort)}:"
            f"{self.cursor_hash(cursor)}:"
            f"{limit}"
        )
