from .api_test_data import get_group_patched_only_users, post_group_only_user, post_user
from .client import client


def test_prevent_groups_deletion():
    # Clean start
    client.delete("/api/v1/groups/g", params={"ignore_users": True})
    client.delete("/api/v1/users/u")

    response = client.post("/api/v1/users", json=post_user)
    assert response.status_code == 201  # user created

    response = client.post("/api/v1/groups", json=post_group_only_user)
    assert response.status_code == 201  # group created
    assert response.json() == get_group_patched_only_users

    response = client.patch("/api/v1/users/u", params={"prevent_groups_deletion": True}, json={"groups": []})
    assert response.status_code == 422  # group would be deleted as it has no attributes

    response = client.delete("/api/v1/users/u", params={"prevent_groups_deletion": True})
    assert response.status_code == 422  # group would be deleted as it has no attributes

    response = client.delete("/api/v1/users/u", params={"prevent_groups_deletion": False})
    assert response.status_code == 204

    response = client.get("/api/v1/groups/g")
    assert response.status_code == 404  # group has been deleted on user deletion as it had no attributes
