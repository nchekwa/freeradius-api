from .api_test_data import get_nas, get_nas_patched, patch_nas, post_nas
from .client import client


def test_nas():
    client.delete("/api/v1/nas/5.5.5.5")

    response = client.get("/api/v1/nas/5.5.5.5")
    assert response.status_code == 404  # NAS not found yet

    response = client.get("/api/v1/nas")
    assert response.status_code == 200
    assert get_nas not in response.json()  # NAS not part of collection yet

    response = client.post("/api/v1/nas", json=post_nas)
    assert response.status_code == 201  # NAS created
    assert response.json() == get_nas

    response = client.post("/api/v1/nas", json=post_nas)
    assert response.status_code == 409  # NAS already exists

    response = client.get("/api/v1/nas/5.5.5.5")
    assert response.status_code == 200  # NAS now found
    assert response.json() == get_nas

    response = client.get("/api/v1/nas")
    assert response.status_code == 200
    # assert get_nas in response.json()  # NAS now part of collection

    response = client.patch("/api/v1/nas/non-existing-nas", json={})
    assert response.status_code == 404

    response = client.patch("/api/v1/nas/5.5.5.5", json=patch_nas)
    assert response.status_code == 200
    assert response.json() == get_nas_patched

    response = client.delete("/api/v1/nas/5.5.5.5")
    assert response.status_code == 204  # NAS deleted

    response = client.delete("/api/v1/nas/5.5.5.5")
    assert response.status_code == 404  # NAS now not found
