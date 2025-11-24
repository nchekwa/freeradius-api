from __future__ import annotations

from ..models import HuntGroup, HuntGroupCreate
from ..params import HuntGroupUpdate
from ..repositories import HuntGroupRepository
from .exceptions import ServiceExceptions


class HuntGroupService:
    def __init__(self, huntgroup_repo: HuntGroupRepository):
        self.huntgroup_repo = huntgroup_repo

    def find(
        self, limit: int | None = 100, groupname_like: str | None = None, groupname_gt: str | None = None
    ) -> list[HuntGroup]:
        return self.huntgroup_repo.find(
            limit=limit,
            groupname_like=groupname_like,
            groupname_gt=groupname_gt,
        )

    def get(self, id: int) -> HuntGroup:
        huntgroup = self.huntgroup_repo.find_one(id)
        if not huntgroup:
            raise ServiceExceptions.HuntGroupNotFound("Given huntgroup entry does not exist")
        return huntgroup

    def create(self, huntgroup: HuntGroupCreate) -> HuntGroup:
        return self.huntgroup_repo.add(
            groupname=huntgroup.groupname,
            nasipaddress=huntgroup.nasipaddress,
            nasportid=huntgroup.nasportid,
        )

    def update(self, id: int, huntgroup_update: HuntGroupUpdate) -> HuntGroup:
        huntgroup = self.huntgroup_repo.find_one(id)
        if not huntgroup:
            raise ServiceExceptions.HuntGroupNotFound("Given huntgroup entry does not exist")

        self.huntgroup_repo.set(
            id=id,
            new_groupname=huntgroup_update.groupname,
            new_nasipaddress=huntgroup_update.nasipaddress,
            new_nasportid=huntgroup_update.nasportid,
        )
        return self.huntgroup_repo.find_one(id)  # type: ignore

    def delete(self, id: int):
        huntgroup = self.huntgroup_repo.find_one(id)
        if not huntgroup:
            raise ServiceExceptions.HuntGroupNotFound("Given huntgroup entry does not exist")
        self.huntgroup_repo.remove(id)

    def delete_by_groupname(self, groupname: str):
        if not self.huntgroup_repo.exists_by_groupname(groupname):
            raise ServiceExceptions.HuntGroupNotFound("Given huntgroup entry does not exist")
        self.huntgroup_repo.remove_by_groupname(groupname)
