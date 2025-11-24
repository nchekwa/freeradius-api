from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Response
from dependencies import GroupServiceDep
from freeradius.models import Group
from models.api_error import error_404, error_409
from freeradius.params import GroupUpdate
from freeradius.services import ServiceExceptions
from settings import API_URL, ITEMS_PER_PAGE

router = APIRouter()


@router.get("/groups", tags=["groups"], status_code=200, response_model=list[Group])
def get_groups(group_service: GroupServiceDep, response: Response, groupname_gt: str | None = None):
    groups = group_service.find(limit=ITEMS_PER_PAGE, groupname_gt=groupname_gt)
    if groups:
        last_groupname = groups[-1].groupname
        response.headers["Link"] = f'<{API_URL}/groups?groupname_gt={last_groupname}>; rel="next"'
    return groups


@router.get("/groups/{groupname}", tags=["groups"], status_code=200, response_model=Group, responses={404: error_404})
def get_group(groupname: str, group_service: GroupServiceDep):
    try:
        return group_service.get(groupname)
    except ServiceExceptions.GroupNotFound as exc:
        raise HTTPException(404, str(exc))


@router.post("/groups", tags=["groups"], status_code=201, response_model=Group, responses={409: error_409})
def post_group(
    group: Group,
    group_service: GroupServiceDep,
    response: Response,
    allow_users_creation: Annotated[
        bool, Query(description="If set to true, nonexistent users will be created during group creation")
    ] = False,
):
    try:
        group_service.create(group=group, allow_users_creation=allow_users_creation)
    except ServiceExceptions.GroupAlreadyExists as exc:
        raise HTTPException(409, str(exc))
    except ServiceExceptions.UserNotFound as exc:
        raise HTTPException(422, str(exc))

    response.headers["Location"] = f"{API_URL}/groups/{group.groupname}"
    return group


@router.delete("/groups/{groupname}", tags=["groups"], status_code=204, responses={404: error_404})
def delete_group(
    groupname: str,
    group_service: GroupServiceDep,
    ignore_users: Annotated[
        bool, Query(description="If set to true, the group will be deleted even if it still has users")
    ] = False,
    prevent_users_deletion: Annotated[
        bool, Query(description="If set to false, group users without any attributes will be deleted")
    ] = True,
):
    try:
        group_service.delete(
            groupname=groupname, ignore_users=ignore_users, prevent_users_deletion=prevent_users_deletion
        )
    except ServiceExceptions.GroupNotFound as exc:
        raise HTTPException(404, str(exc))
    except (ServiceExceptions.GroupStillHasUsers, ServiceExceptions.UserWouldBeDeleted) as exc:
        raise HTTPException(422, str(exc))


@router.patch("/groups/{groupname}", tags=["groups"], status_code=200, response_model=Group, responses={404: error_404})
def patch_group(
    groupname: str,
    group_update: GroupUpdate,
    group_service: GroupServiceDep,
    response: Response,
    allow_users_creation: Annotated[
        bool, Query(description="If set to true, nonexistent users will be created during group modification")
    ] = False,
    prevent_users_deletion: Annotated[
        bool, Query(description="If set to false, group users without any attributes will be deleted")
    ] = True,
):
    try:
        updated_group = group_service.update(
            groupname=groupname,
            group_update=group_update,
            allow_users_creation=allow_users_creation,
            prevent_users_deletion=prevent_users_deletion,
        )
    except ServiceExceptions.GroupNotFound as exc:
        raise HTTPException(404, str(exc))
    except (
        ServiceExceptions.UserNotFound,
        ServiceExceptions.UserWouldBeDeleted,
        ServiceExceptions.GroupWouldBeDeleted,
    ) as exc:
        raise HTTPException(422, str(exc))

    response.headers["Location"] = f"{API_URL}/groups/{groupname}"
    return updated_group
