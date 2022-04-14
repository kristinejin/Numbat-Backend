import pytest
from src.FlaskApp import app
from src.clear import clear, clear_company


@pytest.fixture
def client():
    return app.test_client()


ListOfUsrName = []
companies = []


def test_home(client):
    resp = client.get('/')
    assert resp.status_code == 302


def test_register(client, Account, companyFlask):
    company = client.post('/create/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                   'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
    assert company.status_code == 200
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    assert resp.status_code == 302
    ListOfUsrName.append(Account[0])
    companies.append(companyFlask[0])


def test_login(client, Account, companyFlask):
    company = client.post('/create/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                   'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
    assert company.status_code == 200
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    assert resp.status_code == 302
    resp = client.post(
        '/UserLogin', data={'UserName': Account[0], 'Password': Account[1]})
    assert resp.status_code == 302
    ListOfUsrName.append(Account[0])
    companies.append(companyFlask[0])


def test_clear():
    clear(ListOfUsrName)
    clear_company(companies)
