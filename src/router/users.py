from typing import Annotated

from dependencies import UserServiceDep
from fastapi import APIRouter, HTTPException, Query, Response
from freeradius.models import User
from freeradius.params import UserUpdate
from freeradius.services import ServiceExceptions
from models.api_error import error_404, error_409
from settings import API_URL, ITEMS_PER_PAGE

router = APIRouter()


@router.get("/users", tags=["users"], status_code=200, response_model=list[User])
def get_users(user_service: UserServiceDep, response: Response, username_gt: str | None = None):
    users = user_service.find(limit=ITEMS_PER_PAGE, username_gt=username_gt)
    if users:
        last_username = users[-1].username
        response.headers["Link"] = f'<{API_URL}/users?username_gt={last_username}>; rel="next"'
    return users


@router.get("/users/{username}", tags=["users"], status_code=200, response_model=User, responses={404: error_404})
def get_user(username: str, user_service: UserServiceDep):
    try:
        return user_service.get(username)
    except ServiceExceptions.UserNotFound as exc:
        raise HTTPException(404, str(exc))


@router.post("/users", tags=["users"], status_code=201, response_model=User, responses={409: error_409})
def post_user(
    user: User,
    user_service: UserServiceDep,
    response: Response,
    allow_groups_creation: Annotated[
        bool, Query(description="If set to true, nonexistent groups will be created during user creation")
    ] = False,
):
    try:
        user_service.create(user=user, allow_groups_creation=allow_groups_creation)
    except ServiceExceptions.UserAlreadyExists as exc:
        raise HTTPException(409, str(exc))
    except ServiceExceptions.GroupNotFound as exc:
        raise HTTPException(422, str(exc))

    response.headers["Location"] = f"{API_URL}/users/{user.username}"
    return user


@router.delete("/users/{username}", tags=["users"], status_code=204, responses={404: error_404})
def delete_user(
    username: str,
    user_service: UserServiceDep,
    prevent_groups_deletion: Annotated[
        bool, Query(description="If set to false, user groups without any attributes will be deleted")
    ] = True,
):
    try:
        user_service.delete(username=username, prevent_groups_deletion=prevent_groups_deletion)
    except ServiceExceptions.UserNotFound as exc:
        raise HTTPException(404, str(exc))
    except ServiceExceptions.GroupWouldBeDeleted as exc:
        raise HTTPException(422, str(exc))


@router.patch("/users/{username}", tags=["users"], status_code=200, response_model=User, responses={404: error_404})
def patch_user(
    username: str,
    user_update: UserUpdate,
    user_service: UserServiceDep,
    response: Response,
    allow_groups_creation: Annotated[
        bool, Query(description="If set to true, nonexistent groups will be created during user modification")
    ] = False,
    prevent_groups_deletion: Annotated[
        bool, Query(description="If set to false, user groups without any attributes will be deleted")
    ] = True,
):
    try:
        updated_user = user_service.update(
            username=username,
            user_update=user_update,
            allow_groups_creation=allow_groups_creation,
            prevent_groups_deletion=prevent_groups_deletion,
        )
    except ServiceExceptions.UserNotFound as exc:
        raise HTTPException(404, str(exc))
    except (
        ServiceExceptions.GroupNotFound,
        ServiceExceptions.GroupWouldBeDeleted,
        ServiceExceptions.UserWouldBeDeleted,
    ) as exc:
        raise HTTPException(422, str(exc))

    response.headers["Location"] = f"{API_URL}/users/{username}"
    return updated_user
