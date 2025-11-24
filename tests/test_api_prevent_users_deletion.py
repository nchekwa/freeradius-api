from .api_test_data import get_group, get_user_patched_only_groups, post_group, post_user_only_group
from .client import client


def test_prevent_users_deletion():
    # Clean start
    client.delete("/api/v1/groups/g", params={"ignore_users": True})
    client.delete("/api/v1/users/u")

    response = client.post("/api/v1/groups", json=post_group)
    assert response.status_code == 201  # group created
    assert response.json() == get_group

    response = client.post("/api/v1/users", json=post_user_only_group)
    assert response.status_code == 201  # user created
    assert response.json() == get_user_patched_only_groups

    response = client.patch("/api/v1/groups/g", params={"prevent_users_deletion": True}, json={"users": []})
    assert response.status_code == 422  # user would be deleted as it has no attributes

    response = client.delete("/api/v1/groups/g", params={"ignore_users": True, "prevent_users_deletion": True})
    assert response.status_code == 422  # user would be deleted as it has no attributes

    response = client.delete("/api/v1/groups/g", params={"ignore_users": True, "prevent_users_deletion": False})
    assert response.status_code == 204

    response = client.get("/api/v1/users/u")
    assert response.status_code == 404  # user has been deleted on group deletion as it had no attributes
