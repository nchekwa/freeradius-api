from fastapi import Depends, FastAPI
from auth import verify_key
from middleware.process_time import add_process_time_header
from router import default_router, groups_router, huntgroups_router, nas_router, users_router


# API
app = FastAPI(title="FreeRADIUS REST API", dependencies=[Depends(verify_key)])
app.middleware("http")(add_process_time_header)
app.include_router(default_router)
app.include_router(nas_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(groups_router, prefix="/api/v1")
app.include_router(huntgroups_router, prefix="/api/v1")
