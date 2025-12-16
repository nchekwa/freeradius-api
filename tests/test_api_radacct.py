from .client import client


def test_radacct_get_by_username():
    """Test GET /api/v1/radacct/{username} endpoint"""
    # Test with a username that has no sessions
    response = client.get("/api/v1/radacct/nonexistent-user")
    assert response.status_code == 200
    assert response.json() == []
    assert "X-Total-Count" in response.headers
    assert response.headers["X-Total-Count"] == "0"


def test_radacct_get_by_username_with_limit():
    """Test GET /api/v1/radacct/{username} with limit parameter"""
    response = client.get("/api/v1/radacct/testuser?limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_radacct_get_by_username_with_offset():
    """Test GET /api/v1/radacct/{username} with offset parameter"""
    response = client.get("/api/v1/radacct/testuser?offset=0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_radacct_get_by_username_with_limit_and_offset():
    """Test GET /api/v1/radacct/{username} with both limit and offset"""
    response = client.get("/api/v1/radacct/testuser?limit=5&offset=0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
