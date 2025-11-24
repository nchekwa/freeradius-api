from .api_test_data import post_group, post_user_with_group
from .client import client


def test_delete_user_group():
    # Setup: Ensure group g and user u exist and are linked
    # We attempt to create them. If they exist, we assume they are in correct state or ignore conflict.
    # Ideally we would check or clean first.

    # Clean first to be safe
    client.delete("/api/v1/groups/g", params={"ignore_users": True})
    client.delete("/api/v1/users/u")

    # Create
    client.post("/api/v1/groups", json=post_group)
    client.post("/api/v1/users", json=post_user_with_group)

    response = client.delete("/api/v1/groups/g")
    assert response.status_code == 422  # group still has users

    response = client.delete("/api/v1/users/u")
    assert response.status_code == 204  # user deleted

    response = client.delete("/api/v1/users/u")
    assert response.status_code == 404  # user now not found

    response = client.delete("/api/v1/groups/g")
    assert response.status_code == 204  # group deleted

    response = client.delete("/api/v1/groups/g")
    assert response.status_code == 404  # group now not found
