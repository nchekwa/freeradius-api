from __future__ import annotations

from ..models import Group
from ..params import GroupUpdate
from ..repositories import GroupRepository, UserRepository
from .exceptions import ServiceExceptions


class GroupService:
    def __init__(self, group_repo: GroupRepository, user_repo: UserRepository):
        self.group_repo = group_repo
        self.user_repo = user_repo

    def exists(self, groupname: str) -> bool:
        return self.group_repo.exists(groupname)

    def find_one(self, groupname: str) -> Group | None:
        return self.group_repo.find_one(groupname)

    def find(
        self, limit: int | None = 100, groupname_like: str | None = None, groupname_gt: str | None = None
    ) -> list[Group]:
        groups = self.group_repo.find(limit=limit, groupname_like=groupname_like, groupname_gt=groupname_gt)
        for group in groups:
            group.users_number = self.group_repo.count_users(group.groupname)
        return groups

    def find_groupnames(
        self, limit: int | None = 100, groupname_like: str | None = None, groupname_gt: str | None = None
    ) -> list[str]:
        return self.group_repo.find_groupnames(limit=limit, groupname_like=groupname_like, groupname_gt=groupname_gt)

    def get(self, groupname: str) -> Group:
        group = self.group_repo.find_one(groupname)
        if not group:
            raise ServiceExceptions.GroupNotFound("Given group does not exist")
        group.users_number = self.group_repo.count_users(groupname)
        return group

    def create(self, group: Group, allow_users_creation: bool = False) -> Group:
        if self.group_repo.exists(group.groupname):
            raise ServiceExceptions.GroupAlreadyExists("Given group already exists")

        if not allow_users_creation:
            for groupuser in group.users:
                if not self.user_repo.exists(groupuser.username):
                    raise ServiceExceptions.UserNotFound(
                        f"Given user '{groupuser.username}' does not exist: "
                        "create it first or set 'allow_users_creation' parameter to true",
                    )

        self.group_repo.add(group)
        return group

    def delete(self, groupname: str, ignore_users: bool = False, prevent_users_deletion: bool = True):
        group = self.group_repo.find_one(groupname)
        if not group:
            raise ServiceExceptions.GroupNotFound("Given group does not exist")

        if group.users and not ignore_users:
            raise ServiceExceptions.GroupStillHasUsers(
                "Given group still has users: delete them first or set 'ignore_users' parameter to true"
            )

        if prevent_users_deletion:
            for groupuser in group.users:
                user = self.user_repo.find_one(groupuser.username)
                if user and not (user.checks or user.replies or len(user.groups) > 1):
                    raise ServiceExceptions.UserWouldBeDeleted(
                        f"User '{user.username}' would be deleted as it has no attributes and no other groups: "
                        "delete it first or set 'prevent_users_deletion' parameter to false",
                    )

        self.group_repo.remove(groupname)

    def update(
        self,
        groupname: str,
        group_update: GroupUpdate,
        allow_users_creation: bool = False,
        prevent_users_deletion: bool = True,
    ) -> Group:
        group = self.group_repo.find_one(groupname)
        if not group:
            raise ServiceExceptions.GroupNotFound("Given group does not exist")

        if group_update.users:
            if not allow_users_creation:
                for groupuser in group_update.users:
                    if not self.user_repo.exists(groupuser.username):
                        raise ServiceExceptions.UserNotFound(
                            f"Given user '{groupuser.username}' does not exist: "
                            "create it first or set 'allow_users_creation' parameter to true",
                        )

        if (group_update.users or group_update.users == []) and prevent_users_deletion:
            for groupuser in group.users:
                user = self.user_repo.find_one(groupuser.username)
                if user and not (user.checks or user.replies or len(user.groups) > 1):
                    raise ServiceExceptions.UserWouldBeDeleted(
                        f"User '{user.username}' would be deleted as it has no attributes and no other groups: "
                        "delete it first or set 'prevent_users_deletion' parameter to false",
                    )

        new_checks = group.checks if group_update.checks is None else group_update.checks
        new_replies = group.replies if group_update.replies is None else group_update.replies
        new_users = group.users if group_update.users is None else group_update.users
        if not (new_checks or new_replies or new_users):
            raise ServiceExceptions.GroupWouldBeDeleted("Resulting group would have no attributes and no users")

        self.group_repo.set(
            groupname=groupname,
            new_checks=group_update.checks,
            new_replies=group_update.replies,
            new_users=group_update.users,
        )
        return self.group_repo.find_one(groupname)  # type: ignore
