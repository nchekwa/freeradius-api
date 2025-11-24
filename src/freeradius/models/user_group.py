from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class UserGroup(BaseModel):
    groupname: Annotated[str, StringConstraints(min_length=1)]
    priority: Annotated[int, Field(ge=0)] = 1

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }
