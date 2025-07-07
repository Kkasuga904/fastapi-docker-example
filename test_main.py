from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello_world():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, world"}

def test_hello_name():
    res = client.get("/hello?name=Mike")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, Mike"}

def test_hello_default():
    res = client.get("/hello")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, World"}

def test_hello_empty():
    res = client.get("/hello?name=")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello, "}