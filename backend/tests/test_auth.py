from fastapi.testclient import TestClient

from app.seed.chapter1 import seed_chapter1


def test_signup_login_me_patch(client: TestClient, db_session) -> None:
    seed_chapter1(db_session)
    r = client.post(
        "/api/auth/signup",
        json={
            "username": "tuser1",
            "email": "tuser1@example.com",
            "password": "secretpass1",
            "display_name": "Test User",
        },
    )
    assert r.status_code == 200, r.text
    token = r.json()["token"]
    assert r.json()["user"]["username"] == "tuser1"

    r2 = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["display_name"] == "Test User"

    r3 = client.patch(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"display_name": "New Name", "theme": "light"},
    )
    assert r3.status_code == 200
    assert r3.json()["display_name"] == "New Name"
    assert r3.json()["theme"] == "light"

    r4 = client.post("/api/auth/login", json={"username": "tuser1", "password": "secretpass1"})
    assert r4.status_code == 200
    assert r4.json()["token"]


def test_login_invalid(client: TestClient, db_session) -> None:
    seed_chapter1(db_session)
    client.post(
        "/api/auth/signup",
        json={
            "username": "tuser2",
            "email": "tuser2@example.com",
            "password": "goodpassword",
            "display_name": "U2",
        },
    )
    r = client.post("/api/auth/login", json={"username": "tuser2", "password": "wrong"})
    assert r.status_code == 401
