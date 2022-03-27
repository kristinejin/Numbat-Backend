import pytest
from src.FlaskApp import app

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_login(client):
    resp = client.get('/Login')
    assert resp.status_code == 200

def test_register(client):
    resp = client.get('/Register')
    assert resp.status_code == 200