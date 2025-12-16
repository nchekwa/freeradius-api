from .default import router as default_router
from .groups import router as groups_router
from .nas import router as nas_router
from .users import router as users_router
from .huntgroups import router as huntgroups_router
from .radacct import router as radacct_router

__all__ = [
    "default_router",
    "groups_router",
    "nas_router",
    "users_router",
    "huntgroups_router",
    "radacct_router",
]
