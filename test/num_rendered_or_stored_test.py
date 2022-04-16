import pytest
from src.FlaskApp import app
from test.xml_str import xml_as_string
from src.check_num_render_or_store import checkQuota
import random
import string
# import json
from src.clear import clear, clear_company

ListAccountCreated = []
ListCompanyCreated = []


@pytest.fixture
def client():
    return app.test_client()


def test_store_zero(Account):
    assert checkQuota(Account[0], Account[2], "store") == "Success"


def test_store_one(Account, companyFlask, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    company = client.post('/create/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                   'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5][:3]})
    assert company.status_code == 200
    print(company.get_data)
    #assert json.load(company.get_data())['company_created'] == True
    resp = client.post(
        '/Register', data={
            'UserName': Account[0],
            'Password': Account[1],
            'CompanyCode': companyFlask[5][:3],
            'Email': Account[3]
        }
    )
    assert resp.status_code == 302
    resp = client.post(
        '/Store', data={'FileName': Filename, 'XML': xml_as_string})
    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'store') == 'Success'
    ListCompanyCreated.append(companyFlask[5])
    ListAccountCreated.append(Account[0])


def test_clear():
    clear(ListAccountCreated)
    clear_company(ListCompanyCreated)


"""
def test_store_too_may(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302
    resp = client.post(
        '/Store', data={'FileName': Filename, 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'a', 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'b', 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'c', 'XML': xml_as_string})
    assert resp.status_code == 200
    resp = client.post(
        '/Store', data={'FileName': Filename + 'd', 'XML': xml_as_string})
    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'store') == 'Fail'


# TESTS FOR RENDER WHICH HAS NOT YET BEEN IMPLEMENTED IN THIS BRANCH

def test_render_initial(Account, client):
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302
    assert checkQuota(Account[0], Account[2], 'render') == 'Success'


def test_render_success(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302

    resp = client.post(
        '/Store', data={'FileName': Filename, 'XML': xml_as_string})
    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'store') == 'Success'

    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})

    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'render') == 'Success'


def test_render_too_many(Account, client):
    Filename = (''.join(random.choice(string.ascii_lowercase)
                        for i in range(9)))
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
    assert resp.status_code == 302

    resp = client.post(
        '/Store', data={'FileName': Filename, 'XML': xml_as_string})
    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'store') == 'Success'

    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})
    assert resp.status_code == 200
    resp = client.post(
        '/Render', data={'FileName': Filename, 'FileType': "pdf"})
    assert resp.status_code == 200
    assert checkQuota(Account[0], Account[2], 'render') == 'Fail'
"""
