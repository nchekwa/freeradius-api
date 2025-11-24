from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response

from dependencies import HuntGroupServiceDep
from freeradius.models import HuntGroup, HuntGroupCreate
from freeradius.params import HuntGroupUpdate
from freeradius.services import ServiceExceptions
from models.api_error import error_404
from settings import API_URL, ITEMS_PER_PAGE


router = APIRouter()


@router.get("/huntgroups", tags=["huntgroups"], status_code=200, response_model=list[HuntGroup])
def get_huntgroups(
    huntgroup_service: HuntGroupServiceDep,
    response: Response,
    groupname_gt: str | None = None,
    groupname_like: Annotated[str | None, Query()] = None,
):
    huntgroups = huntgroup_service.find(
        limit=ITEMS_PER_PAGE,
        groupname_like=groupname_like,
        groupname_gt=groupname_gt,
    )
    if huntgroups:
        last_groupname = huntgroups[-1].groupname
        response.headers["Link"] = f'<{API_URL}/huntgroups?groupname_gt={last_groupname}>; rel="next"'
    return huntgroups


@router.get(
    "/huntgroups/{id}",
    tags=["huntgroups"],
    status_code=200,
    response_model=HuntGroup,
    responses={404: error_404},
)
def get_huntgroup(id: int, huntgroup_service: HuntGroupServiceDep):
    try:
        return huntgroup_service.get(id)
    except ServiceExceptions.HuntGroupNotFound as exc:
        raise HTTPException(404, str(exc))


@router.post(
    "/huntgroups",
    tags=["huntgroups"],
    status_code=201,
    response_model=HuntGroup,
)
def post_huntgroup(huntgroup: HuntGroupCreate, huntgroup_service: HuntGroupServiceDep, response: Response):
    created = huntgroup_service.create(huntgroup)
    response.headers["Location"] = f"{API_URL}/huntgroups/{created.id}"
    return created


@router.patch(
    "/huntgroups/{id}",
    tags=["huntgroups"],
    status_code=200,
    response_model=HuntGroup,
    responses={404: error_404},
)
def patch_huntgroup(
    id: int,
    huntgroup_update: HuntGroupUpdate,
    huntgroup_service: HuntGroupServiceDep,
    response: Response,
):
    try:
        updated_huntgroup = huntgroup_service.update(id=id, huntgroup_update=huntgroup_update)
    except ServiceExceptions.HuntGroupNotFound as exc:
        raise HTTPException(404, str(exc))

    response.headers["Location"] = f"{API_URL}/huntgroups/{id}"
    return updated_huntgroup


@router.delete(
    "/huntgroups/{id}",
    tags=["huntgroups"],
    status_code=204,
    responses={404: error_404},
)
def delete_huntgroup(id: int, huntgroup_service: HuntGroupServiceDep):
    try:
        huntgroup_service.delete(id)
    except ServiceExceptions.HuntGroupNotFound as exc:
        raise HTTPException(404, str(exc))


@router.delete(
    "/huntgroups/by-groupname/{groupname}",
    tags=["huntgroups"],
    status_code=204,
    responses={404: error_404},
)
def delete_huntgroups_by_groupname(groupname: str, huntgroup_service: HuntGroupServiceDep):
    try:
        huntgroup_service.delete_by_groupname(groupname)
    except ServiceExceptions.HuntGroupNotFound as exc:
        raise HTTPException(404, str(exc))
