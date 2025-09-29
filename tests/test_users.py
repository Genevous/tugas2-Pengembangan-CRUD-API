import pytest
from fastapi.testclient import TestClient
from main import app
from modules.users.routes.createUser import USERS, NEXT_ID

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_data():
    USERS.clear()
    NEXT_ID["val"] = 1
    yield
    USERS.clear()
    NEXT_ID["val"] = 1

# CREATE
def test_create_user_success():
    payload = {"username": "johndoe","email": "john@example.com","password": "Abcd1234!","role": "staff"}
    r = client.post("/users", json=payload)
    assert r.status_code == 201

def test_create_invalid_username():
    payload = {"username": "abc","email": "abc@example.com","password": "Abcd1234!","role": "staff"}
    r = client.post("/users", json=payload)
    assert r.status_code == 422

def test_create_invalid_password():
    payload = {"username": "validuser","email": "v@example.com","password": "abcdef12","role": "staff"}
    r = client.post("/users", json=payload)
    assert r.status_code == 422

def test_create_duplicate_username():
    payload = {"username": "dupuser","email": "dup@example.com","password": "Dupuser1!","role": "staff"}
    client.post("/users", json=payload)
    r = client.post("/users", json=payload)
    assert r.status_code == 400

# READ
def test_read_all_admin():
    client.post("/users", json={"username": "admin1","email": "a@a.com","password": "Admin123!","role": "admin"})
    r = client.get("/users", headers={"x-user-role": "admin"})
    assert r.status_code == 200

def test_read_all_staff_forbidden():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.get("/users", headers={"x-user-role": "staff", "x-user-id": "1"})
    assert r.status_code == 403

def test_read_user_admin():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.get("/users/1", headers={"x-user-role": "admin"})
    assert r.status_code == 200

def test_read_user_staff_own():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.get("/users/1", headers={"x-user-role": "staff", "x-user-id": "1"})
    assert r.status_code == 200

def test_read_user_staff_other_forbidden():
    client.post("/users", json={"username": "staff1","email": "s1@s.com","password": "Staff123!","role": "staff"})
    client.post("/users", json={"username": "staff2","email": "s2@s.com","password": "Staff123!","role": "staff"})
    r = client.get("/users/2", headers={"x-user-role": "staff", "x-user-id": "1"})
    assert r.status_code == 403

def test_read_user_notfound():
    r = client.get("/users/999", headers={"x-user-role": "admin"})
    assert r.status_code == 404

# UPDATE
def test_update_user_admin():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.put("/users/1", headers={"x-user-role": "admin"}, json={"username": "updated"})
    assert r.status_code == 200
    assert r.json()["username"] == "updated"

def test_update_user_notfound():
    r = client.put("/users/99", headers={"x-user-role": "admin"}, json={"username": "nouser"})
    assert r.status_code == 404

def test_update_user_staff_forbidden():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.put("/users/1", headers={"x-user-role": "staff", "x-user-id": "1"}, json={"username": "newname"})
    assert r.status_code == 403

# DELETE
def test_delete_user_admin():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.delete("/users/1", headers={"x-user-role": "admin"})
    assert r.status_code == 200

def test_delete_user_notfound():
    r = client.delete("/users/123", headers={"x-user-role": "admin"})
    assert r.status_code == 404

def test_delete_user_staff_forbidden():
    client.post("/users", json={"username": "staff1","email": "s@s.com","password": "Staff123!","role": "staff"})
    r = client.delete("/users/1", headers={"x-user-role": "staff", "x-user-id": "1"})
    assert r.status_code == 403
