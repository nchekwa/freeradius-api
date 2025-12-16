from datetime import datetime
from pydantic import BaseModel


class RadAcct(BaseModel):
    radacctid: int
    acctsessionid: str = ""
    acctuniqueid: str = ""
    username: str = ""
    realm: str | None = ""
    nasipaddress: str = ""
    nasportid: str | None = None
    nasporttype: str | None = None
    acctstarttime: datetime | None = None
    acctupdatetime: datetime | None = None
    acctstoptime: datetime | None = None
    acctinterval: int | None = None
    acctsessiontime: int | None = None
    acctauthentic: str | None = None
    connectinfo_start: str | None = None
    connectinfo_stop: str | None = None
    acctinputoctets: int | None = None
    acctoutputoctets: int | None = None
    calledstationid: str = ""
    callingstationid: str = ""
    acctterminatecause: str = ""
    servicetype: str | None = None
    framedprotocol: str | None = None
    framedipaddress: str = ""
    framedipv6address: str = ""
    framedipv6prefix: str = ""
    framedinterfaceid: str = ""
    delegatedipv6prefix: str = ""
    class_attr: str | None = None

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "json_schema_extra": {
            "examples": [
                {
                    "radacctid": 1,
                    "acctsessionid": "session123",
                    "acctuniqueid": "unique123",
                    "username": "testuser",
                    "nasipaddress": "192.168.1.1",
                    "acctstarttime": "2024-01-01T10:00:00",
                    "acctsessiontime": 3600,
                    "framedipaddress": "10.0.0.1",
                }
            ]
        },
    }
