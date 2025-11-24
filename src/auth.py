import os
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader

_header_name = os.getenv("X_API_KEY_HEADER", "X-API-Key")
_x_api_key_header = APIKeyHeader(name=_header_name, auto_error=False)

_env_api_key = os.getenv("X_API_KEY")

if _env_api_key and "," in _env_api_key:
    _x_api_key = [key.strip() for key in _env_api_key.split(",")]
else:
    _x_api_key = _env_api_key


async def verify_key(x_api_key: Optional[str] = Depends(_x_api_key_header)):
    if _x_api_key:
        if x_api_key is None:
            raise HTTPException(403, "Not authenticated")

        if isinstance(_x_api_key, list):
            if x_api_key not in _x_api_key:
                raise HTTPException(401, "Invalid key")
        elif x_api_key != _x_api_key:
            raise HTTPException(401, "Invalid key")
