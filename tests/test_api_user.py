from .api_test_data import (
    get_user,
    get_user_patched_only_checks,
    get_user_patched_only_groups,
    get_user_patched_only_replies,
    patch_user_bad_group,
    patch_user_dup_group,
    patch_user_only_checks,
    patch_user_only_groups,
    patch_user_only_replies,
    post_group,
    post_user_bad_group,
    post_user_with_group,
)
from .client import client


def test_user():
    client.delete("/api/v1/groups/g", params={"ignore_users": True})
    client.delete("/api/v1/users/u")
    # Ensure group g exists for user creation
    client.post("/api/v1/groups", json=post_group)

    response = client.get("/api/v1/users/u")
    assert response.status_code == 404  # user not found yet

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert get_user not in response.json()  # user not part of collection yet

    response = client.post("/api/v1/users", json=post_user_bad_group)
    assert response.status_code == 422  # group does not exist

    response = client.post("/api/v1/users", json=post_user_with_group)
    assert response.status_code == 201  # user created
    assert response.json() == get_user

    response = client.post("/api/v1/users", json=post_user_with_group)
    assert response.status_code == 409  # user already exists

    response = client.get("/api/v1/users/u")
    assert response.status_code == 200  # user now found
    assert response.json() == get_user

    response = client.get("/api/v1/users")
    assert response.status_code == 200
    # Check if user is in collection by finding it and comparing
    users = response.json()
    found_user = next((u for u in users if u["username"] == get_user["username"]), None)
    assert found_user is not None, f"User {get_user['username']} not found in response"
    assert found_user == get_user  # user now part of collection

    # patch operation

    response = client.patch("/api/v1/users/non-existing-user", json={})
    assert response.status_code == 404  # user not found

    response = client.patch("/api/v1/users/u", json=patch_user_bad_group)
    assert response.status_code == 422  # group does not exist

    response = client.patch("/api/v1/users/u", json=patch_user_dup_group)
    assert response.status_code == 422  # given groups have one or more duplicates

    response = client.patch("/api/v1/users/u", json={"replies": [], "checks": [], "groups": []})
    assert response.status_code == 422  # resulting user would have no attributes

    response = client.patch("/api/v1/users/u", json=patch_user_only_checks)
    assert response.status_code == 200
    assert response.json() == get_user_patched_only_checks

    response = client.patch("/api/v1/users/u", json={"checks": []})
    assert response.status_code == 422  # resulting user would have no attributes and no groups

    response = client.patch("/api/v1/users/u", json=patch_user_only_replies)
    assert response.status_code == 200
    assert response.json() == get_user_patched_only_replies

    response = client.patch("/api/v1/users/u", json={"replies": []})
    assert response.status_code == 422  # resulting user would have no attributes and no groups

    response = client.patch("/api/v1/users/u", json=patch_user_only_groups)
    assert response.status_code == 200
    assert response.json() == get_user_patched_only_groups

    response = client.patch("/api/v1/users/u", json={"groups": []})
    assert response.status_code == 422  # resulting user would have no attributes and no groups
