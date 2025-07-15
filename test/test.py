import pytest
import time
import requests

BASE = "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    # give docker-compose a moment
    time.sleep(5)
    yield

def test_crud_flow():
    item = {"id": 1, "name": "Foo", "description": "Bar"}

    # CREATE
    r = requests.post(f"{BASE}/items/", json=item)
    assert r.status_code == 201
    assert r.json() == item

    # READ
    r = requests.get(f"{BASE}/items/1")
    assert r.status_code == 200

    # UPDATE
    updated = {"id": 1, "name": "FooX", "description": "Baz"}
    r = requests.put(f"{BASE}/items/1", json=updated)
    assert r.status_code == 200
    assert r.json()["name"] == "FooX"

    # DELETE
    r = requests.delete(f"{BASE}/items/1")
    assert r.status_code == 204

    # NOT FOUND
    r = requests.get(f"{BASE}/items/1")
    assert r.status_code == 404
