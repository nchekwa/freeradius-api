from __future__ import annotations

from ..models import User
from ..params import UserUpdate
from ..repositories import GroupRepository, UserRepository
from .exceptions import ServiceExceptions


class UserService:
    def __init__(self, user_repo: UserRepository, group_repo: GroupRepository):
        self.user_repo = user_repo
        self.group_repo = group_repo

    def exists(self, username: str) -> bool:
        return self.user_repo.exists(username)

    def find_one(self, username: str) -> User | None:
        return self.user_repo.find_one(username)

    def find(
        self, limit: int | None = 100, username_like: str | None = None, username_gt: str | None = None
    ) -> list[User]:
        return self.user_repo.find(limit=limit, username_like=username_like, username_gt=username_gt)

    def find_usernames(
        self, limit: int | None = 100, username_like: str | None = None, username_gt: str | None = None
    ) -> list[str]:
        return self.user_repo.find_usernames(limit=limit, username_like=username_like, username_gt=username_gt)

    def get(self, username: str) -> User:
        user = self.user_repo.find_one(username)
        if not user:
            raise ServiceExceptions.UserNotFound("Given user does not exist")
        return user

    def create(self, user: User, allow_groups_creation: bool = False) -> User:
        if self.user_repo.exists(user.username):
            raise ServiceExceptions.UserAlreadyExists("Given user already exists")

        if not allow_groups_creation:
            for usergroup in user.groups:
                if not self.group_repo.exists(usergroup.groupname):
                    raise ServiceExceptions.GroupNotFound(
                        f"Given group '{usergroup.groupname}' does not exist: "
                        "create it first or set 'allow_groups_creation' parameter to true",
                    )

        self.user_repo.add(user)
        return user

    def delete(self, username: str, prevent_groups_deletion: bool = True):
        user = self.user_repo.find_one(username)
        if not user:
            raise ServiceExceptions.UserNotFound("Given user does not exist")

        if prevent_groups_deletion:
            for usergroup in user.groups:
                group = self.group_repo.find_one(usergroup.groupname)
                if group and not (group.checks or group.replies or len(group.users) > 1):
                    raise ServiceExceptions.GroupWouldBeDeleted(
                        f"Group '{group.groupname}' would be deleted as it has no attributes and no other users: "
                        "delete it first or set 'prevent_groups_deletion' parameter to false",
                    )

        self.user_repo.remove(username)

    def update(
        self,
        username: str,
        user_update: UserUpdate,
        allow_groups_creation: bool = False,
        prevent_groups_deletion: bool = True,
    ) -> User:
        user = self.user_repo.find_one(username)
        if not user:
            raise ServiceExceptions.UserNotFound("Given user does not exist")

        if user_update.groups:
            if not allow_groups_creation:
                for usergroup in user_update.groups:
                    if not self.group_repo.exists(usergroup.groupname):
                        raise ServiceExceptions.GroupNotFound(
                            f"Given group '{usergroup.groupname}' does not exist: "
                            "create it first or set 'allow_groups_creation' parameter to true",
                        )

        if (user_update.groups or user_update.groups == []) and prevent_groups_deletion:
            for usergroup in user.groups:
                group = self.group_repo.find_one(usergroup.groupname)
                if group and not (group.checks or group.replies or len(group.users) > 1):
                    raise ServiceExceptions.GroupWouldBeDeleted(
                        f"Group '{group.groupname}' would be deleted as it has no attributes and no other users: "
                        "delete it first or set 'prevent_groups_deletion' parameter to false",
                    )

        new_checks = user.checks if user_update.checks is None else user_update.checks
        new_replies = user.replies if user_update.replies is None else user_update.replies
        new_groups = user.groups if user_update.groups is None else user_update.groups
        if not (new_checks or new_replies or new_groups):
            raise ServiceExceptions.UserWouldBeDeleted("Resulting user would have no attributes and no groups")

        self.user_repo.set(
            username=username,
            new_checks=user_update.checks,
            new_replies=user_update.replies,
            new_groups=user_update.groups,
        )
        return self.user_repo.find_one(username)  # type: ignore
