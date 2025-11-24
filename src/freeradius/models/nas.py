from typing import Annotated
from pydantic import BaseModel, StringConstraints


class Nas(BaseModel):
    nasname: Annotated[str, StringConstraints(min_length=1)]
    shortname: Annotated[str, StringConstraints(min_length=1)]
    secret: Annotated[str, StringConstraints(min_length=1)]

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "json_schema_extra": {
            "examples": [
                {
                    "nasname": "5.5.5.5",
                    "shortname": "my-nas",
                    "secret": "my-secret",
                }
            ]
        },
    }


# https://networkradius.com/doc/current/raddb/clients.html
# Nas Types:
# cisco
# computone
# livingston
# juniper
# max40xx
# multitech
# netserver
# pathras
# patton
# portslave
# tc
# usrhiper
# other (for all other types)
