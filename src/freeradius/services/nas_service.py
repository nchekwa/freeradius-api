from __future__ import annotations

from ..models import Nas
from ..params import NasUpdate
from ..repositories import NasRepository
from .exceptions import ServiceExceptions


class NasService:
    def __init__(self, nas_repo: NasRepository):
        self.nas_repo = nas_repo

    def exists(self, nasname: str) -> bool:
        return self.nas_repo.exists(nasname)

    def find_one(self, nasname: str) -> Nas | None:
        return self.nas_repo.find_one(nasname)

    def find(
        self, limit: int | None = 100, nasname_like: str | None = None, nasname_gt: str | None = None
    ) -> list[Nas]:
        return self.nas_repo.find(limit=limit, nasname_like=nasname_like, nasname_gt=nasname_gt)

    def find_nasnames(
        self, limit: int | None = 100, nasname_like: str | None = None, nasname_gt: str | None = None
    ) -> list[str]:
        return self.nas_repo.find_nasnames(limit=limit, nasname_like=nasname_like, nasname_gt=nasname_gt)

    def get(self, nasname: str) -> Nas:
        nas = self.nas_repo.find_one(nasname)
        if not nas:
            raise ServiceExceptions.NasNotFound("Given NAS does not exist")
        return nas

    def create(self, nas: Nas) -> Nas:
        if self.nas_repo.exists(nas.nasname):
            raise ServiceExceptions.NasAlreadyExists("Given NAS already exists")
        self.nas_repo.add(nas)
        return nas

    def delete(self, nasname: str):
        if not self.nas_repo.exists(nasname):
            raise ServiceExceptions.NasNotFound("Given NAS does not exist")
        self.nas_repo.remove(nasname)

    def update(self, nasname: str, nas_update: NasUpdate) -> Nas:
        nas = self.nas_repo.find_one(nasname)
        if not nas:
            raise ServiceExceptions.NasNotFound("Given NAS does not exist")
        self.nas_repo.set(nasname, new_shortname=nas_update.shortname, new_secret=nas_update.secret)
        return self.nas_repo.find_one(nasname)  # type: ignore
