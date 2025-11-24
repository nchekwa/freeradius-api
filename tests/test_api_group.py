from .api_test_data import (
    get_group,
    get_group_patched_only_checks,
    get_group_patched_only_replies,
    get_group_patched_only_users,
    patch_group_bad_user,
    patch_group_dup_user,
    patch_group_only_checks,
    patch_group_only_replies,
    patch_group_only_users,
    post_group,
    post_group_bad_user,
    post_user,
)
from .client import client


def test_group():
    client.delete("/api/v1/groups/g", params={"ignore_users": True})
    client.delete("/api/v1/users/u")

    response = client.get("/api/v1/groups/g")
    assert response.status_code == 404  # group not found yet

    response = client.get("/api/v1/groups")
    assert response.status_code == 200
    assert get_group not in response.json()  # group not part of collection yet

    response = client.post("/api/v1/groups", json=post_group_bad_user)
    assert response.status_code == 422  # user does not exist

    response = client.post("/api/v1/groups", json=post_group)
    assert response.status_code == 201  # group created
    assert response.json() == get_group

    response = client.post("/api/v1/groups", json=post_group)
    assert response.status_code == 409  # group already exists

    response = client.get("/api/v1/groups/g")
    assert response.status_code == 200  # group now found
    assert response.json() == get_group

    response = client.get("/api/v1/groups")
    assert response.status_code == 200
    assert get_group in response.json()  # group now part of collection

    # patch operation

    response = client.patch("/api/v1/groups/non-existing-group", json={})
    assert response.status_code == 404  # group not found

    response = client.patch("/api/v1/groups/g", json=patch_group_bad_user)
    assert response.status_code == 422  # user does not exist

    response = client.patch("/api/v1/groups/g", json=patch_group_dup_user)
    assert response.status_code == 422  # given users have one or more duplicates

    response = client.patch("/api/v1/groups/g", json={"checks": [], "replies": [], "users": []})
    assert response.status_code == 422  # resulting group would have no attributes and no users

    response = client.post("/api/v1/users", json=post_user)
    assert response.status_code == 201  # user created, in order to add it in the group

    response = client.patch("/api/v1/groups/g", json=patch_group_only_users)
    assert response.status_code == 200
    assert response.json() == get_group_patched_only_users

    response = client.patch("/api/v1/groups/g", json={"users": []})
    assert response.status_code == 422  # resulting group would have no attributes and no users

    response = client.patch("/api/v1/groups/g", json=patch_group_only_checks)
    assert response.status_code == 200
    assert response.json() == get_group_patched_only_checks

    response = client.patch("/api/v1/groups/g", json={"checks": []})
    assert response.status_code == 422  # resulting group would have no attributes and no users

    response = client.patch("/api/v1/groups/g", json=patch_group_only_replies)
    assert response.status_code == 200
    assert response.json() == get_group_patched_only_replies

    response = client.patch("/api/v1/groups/g", json={"replies": []})
    assert response.status_code == 422  # resulting group would have no attributes and no users

    response = client.delete("/api/v1/users/u")
    assert response.status_code == 204  # user deleted
