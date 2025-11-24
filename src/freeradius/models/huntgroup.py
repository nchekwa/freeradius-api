from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class HuntGroup(BaseModel):
    id: Annotated[int, Field(ge=1)]
    groupname: Annotated[str, StringConstraints(min_length=1)]
    nasipaddress: Annotated[str, StringConstraints(min_length=1)]
    nasportid: Annotated[str, StringConstraints(min_length=0)] = ""

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }


class HuntGroupCreate(BaseModel):
    groupname: Annotated[str, StringConstraints(min_length=1)]
    nasipaddress: Annotated[str, StringConstraints(min_length=1)]
    nasportid: Annotated[str, StringConstraints(min_length=0)] = ""

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }
