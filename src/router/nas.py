from fastapi import APIRouter, HTTPException, Response
from dependencies import NasServiceDep
from freeradius.models import Nas
from models.api_error import error_404, error_409
from freeradius.params import NasUpdate
from freeradius.services import ServiceExceptions
from settings import API_URL, ITEMS_PER_PAGE


router = APIRouter()


@router.get("/nas", tags=["nas"], status_code=200, response_model=list[Nas])
def get_nases(nas_service: NasServiceDep, response: Response, nasname_gt: str | None = None):
    nas = nas_service.find(limit=ITEMS_PER_PAGE, nasname_gt=nasname_gt)
    if nas:
        last_nasname = nas[-1].nasname
        response.headers["Link"] = f'<{API_URL}/nas?nasname_gt={last_nasname}>; rel="next"'
    return nas


@router.get("/nas/{nasname}", tags=["nas"], status_code=200, response_model=Nas, responses={404: error_404})
def get_nas(nasname: str, nas_service: NasServiceDep):
    try:
        return nas_service.get(nasname)
    except ServiceExceptions.NasNotFound as exc:
        raise HTTPException(404, str(exc))


@router.post("/nas", tags=["nas"], status_code=201, response_model=Nas, responses={409: error_409})
def post_nas(nas: Nas, nas_service: NasServiceDep, response: Response):
    try:
        nas_service.create(nas)
    except ServiceExceptions.NasAlreadyExists as exc:
        raise HTTPException(409, str(exc))

    response.headers["Location"] = f"{API_URL}/nas/{nas.nasname}"
    return nas


@router.delete("/nas/{nasname}", tags=["nas"], status_code=204, responses={404: error_404})
def delete_nas(nasname: str, nas_service: NasServiceDep):
    try:
        nas_service.delete(nasname)
    except ServiceExceptions.NasNotFound as exc:
        raise HTTPException(404, str(exc))


@router.patch("/nas/{nasname}", tags=["nas"], status_code=200, response_model=Nas, responses={404: error_404})
def patch_nas(nasname: str, nas_update: NasUpdate, nas_service: NasServiceDep, response: Response):
    try:
        updated_nas = nas_service.update(nasname=nasname, nas_update=nas_update)
    except ServiceExceptions.NasNotFound as exc:
        raise HTTPException(404, str(exc))

    response.headers["Location"] = f"{API_URL}/nas/{nasname}"
    return updated_nas
