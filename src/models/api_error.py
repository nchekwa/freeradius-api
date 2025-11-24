from pydantic import BaseModel


class RadAPIError(BaseModel):
    detail: str

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
    }


error_404 = {"model": RadAPIError, "description": "Item not found"}
error_409 = {"model": RadAPIError, "description": "Item already exists"}
