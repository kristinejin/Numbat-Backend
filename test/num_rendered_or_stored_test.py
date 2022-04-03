import pytest
from src.FlaskApp import app
from test.xml_str import xml_as_string
from src.check_num_render_or_store import check_okay
import random
import string


@pytest.fixture
def client():
    return app.test_client()


def test_store_zero(Account):
    assert check_okay(Account[0], Account[2], "store") == "Success"


def test_store_one(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302
    resp = client.post(
        '/Store', data={'FileName': Filename, 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'store') == 'Success'


def test_store_too_may(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302
    resp = client.post(
        '/Store', data={'FileName': Filename, 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'a', 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'b', 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'c', 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'd', 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'store') == 'Fail'


# TESTS FOR RENDER WHICH HAS NOT YET BEEN IMPLEMENTED IN THIS BRANCH

def test_render_initial(Account, client):
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302
    assert check_okay(Account[0], Account[2], 'render') == 'Success'


def test_render_success(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302

    resp = client.post(
        '/Store', data={'FileName': Filename, 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'store') == 'Success'

    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})

    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'render') == 'Success'


def test_render_too_many(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                        for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302

    resp = client.post(
        '/Store', data={'FileName': Filename, 'Password': Account[2], 'XML': xml_as_string})
    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'store') == 'Success'

    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'Password': Account[2], 'FileType': "pdf"})
    assert resp.status_code == 200
    assert check_okay(Account[0], Account[2], 'render') == 'Fail'
