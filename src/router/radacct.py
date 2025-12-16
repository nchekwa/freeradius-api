from typing import Annotated

from dependencies import RadAcctServiceDep
from fastapi import APIRouter, Query, Response
from freeradius.models import RadAcct
from settings import API_URL, ITEMS_PER_PAGE

router = APIRouter()


@router.get(
    "/radacct/{username}",
    tags=["radacct"],
    status_code=200,
    response_model=list[RadAcct],
)
def get_radacct_by_username(
    username: str,
    radacct_service: RadAcctServiceDep,
    response: Response,
    limit: Annotated[int, Query(description="Maximum number of records to return", ge=1, le=1000)] = ITEMS_PER_PAGE,
    offset: Annotated[int | None, Query(description="Number of records to skip")] = None,
):
    """
    Get accounting sessions for a specific username.
    Returns a list of accounting records ordered by start time (most recent first).
    """
    sessions = radacct_service.find_by_username(username=username, limit=limit, offset=offset)
    total_count = radacct_service.count_by_username(username)
    response.headers["X-Total-Count"] = str(total_count)
    return sessions
