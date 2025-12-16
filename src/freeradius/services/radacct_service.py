from __future__ import annotations

from ..models import RadAcct
from ..repositories import RadAcctRepository


class RadAcctService:
    def __init__(self, radacct_repo: RadAcctRepository):
        self.radacct_repo = radacct_repo

    def find_by_username(
        self,
        username: str,
        limit: int | None = 100,
        offset: int | None = None,
    ) -> list[RadAcct]:
        return self.radacct_repo.find_by_username(
            username=username,
            limit=limit,
            offset=offset,
        )

    def count_by_username(self, username: str) -> int:
        return self.radacct_repo.count_by_username(username)
