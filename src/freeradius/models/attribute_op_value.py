from typing import Annotated
from pydantic import BaseModel, StringConstraints


class AttributeOpValue(BaseModel):
    attribute: Annotated[str, StringConstraints(min_length=1)]
    op: Annotated[str, StringConstraints(min_length=1)]
    value: Annotated[str, StringConstraints(min_length=1)]

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }
