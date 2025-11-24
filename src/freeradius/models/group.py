from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints, model_validator
from .attribute_op_value import AttributeOpValue
from .group_user import GroupUser


class Group(BaseModel):
    groupname: Annotated[str, StringConstraints(min_length=1)]
    checks: list[AttributeOpValue] = []
    replies: list[AttributeOpValue] = []
    users_number: int = 0
    users: list[GroupUser] = Field(default_factory=list, exclude=True)

    @model_validator(mode="after")
    def check_fields_on_init(self):
        if not (self.checks or self.replies or self.users):
            raise ValueError(
                "Group must have at least one check or one reply attribute, or must have at least one user"
            )

        usernames = [user.username for user in self.users]
        if not len(usernames) == len(set(usernames)):
            raise ValueError("Given users have one or more duplicates")

        return self

    def contains_user(self, username: str) -> bool:
        for user in self.users:
            if user.username == username:
                return True
        return False

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "json_schema_extra": {
            "examples": [
                {
                    "groupname": "my-group",
                    "replies": [AttributeOpValue(attribute="Filter-Id", op=":=", value="10m").model_dump()],
                }
            ]
        },
    }
