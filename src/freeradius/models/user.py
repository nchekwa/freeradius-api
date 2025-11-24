from typing import Annotated
from pydantic import BaseModel, StringConstraints, model_validator
from .attribute_op_value import AttributeOpValue
from .user_group import UserGroup


class User(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1)]
    checks: list[AttributeOpValue] = []
    replies: list[AttributeOpValue] = []
    groups: list[UserGroup] = []

    @model_validator(mode="after")
    def check_fields_on_init(self):
        if not (self.checks or self.replies or self.groups):
            raise ValueError(
                "User must have at least one check or one reply attribute, or must have at least one group"
            )

        groupnames = [group.groupname for group in self.groups]
        if not len(groupnames) == len(set(groupnames)):
            raise ValueError("Given groups have one or more duplicates")

        return self

    def belongs_to_group(self, groupname: str) -> bool:
        for group in self.groups:
            if group.groupname == groupname:
                return True
        return False

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "json_schema_extra": {
            "examples": [
                {
                    "username": "my-user",
                    "checks": [AttributeOpValue(attribute="Cleartext-Password", op=":=", value="my-pass").model_dump()],
                    "replies": [
                        AttributeOpValue(attribute="Framed-IP-Address", op=":=", value="10.0.0.1").model_dump(),
                        AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.1.0/24").model_dump(),
                        AttributeOpValue(attribute="Framed-Route", op="+=", value="192.168.2.0/24").model_dump(),
                        AttributeOpValue(attribute="Huawei-Vpn-Instance", op=":=", value="my-vrf").model_dump(),
                    ],
                    "groups": [UserGroup(groupname="my-group").model_dump()],
                }
            ]
        },
    }
