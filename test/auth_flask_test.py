import pytest
from src.FlaskApp import app
from src.clear import clear

@pytest.fixture
def client():
    return app.test_client()


ListOfUsrName = []

def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 302

def test_login(client,Account):
    resp = client.get('/Register')
    assert resp.status_code == 200
    resp = client.post('/Register', data={'UserName': Account[0], 'Password': Account[1]})
    assert resp.status_code == 302
    resp = client.get('/UserLogin')
    assert resp.status_code == 200
    resp = client.post('/UserLogin', data={'UserName': Account[0], 'Password': Account[1]})
    assert resp.status_code == 302
    ListOfUsrName.append(Account[0])

def test_register(client,Account):
    resp = client.get('/Register')
    assert resp.status_code == 200
    resp = client.post('/Register', data={'UserName': Account[0], 'Password': Account[1]})
    assert resp.status_code == 302
    ListOfUsrName.append(Account[0])



def test_clear():
    clear(ListOfUsrName)
    pass