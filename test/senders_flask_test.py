import pytest
from src.FlaskApp import app
from src.clear import clear, clear_company
# import json


@pytest.fixture
def client():
    return app.test_client()


userList = []
companyList = []


def test_add_and_remove_sender(client, Account, companyFlask, companyFlask2):
    company1 = client.post('/register/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                      'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
    assert company1.status_code == 200
    companyList.append(companyFlask[0])
    company2 = client.post('/register/company', data={'name': companyFlask2[0], 'abn': companyFlask2[1], 'street': companyFlask2[2],
                                                      'suburb': companyFlask2[3], 'postcode': companyFlask2[4], 'companyCode': companyFlask2[5]})
    assert company2.status_code == 200
    companyList.append(companyFlask2[0])
    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    assert resp.status_code == 200
    userList.append(Account[0])
    add = client.post(
        '/senders/add', data={'senderName': companyFlask2[0]})
    assert add.status_code == 200
    remove = client.delete(
        '/senders/remove', data={'senderName': companyFlask2[0]})
    assert remove.status_code == 200


"""
def test_create(client, Account, companyFlask):
    company1 = client.post('/register/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                      'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
    assert company1.status_code == 200
    companyList.append(companyFlask[0])

    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    assert resp.status_code == 200
    userList.append(Account[0])
"""

"""
def test_send(client, Account, companyFlask, companyFlask2):
    company1 = client.post('/register/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
                                                      'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
    assert company1.status_code == 200
    companyList.append(companyFlask[0])

    company2 = client.post('/register/company', data={'name': companyFlask2[0], 'abn': companyFlask2[1], 'street': companyFlask2[2],
                                                      'suburb': companyFlask2[3], 'postcode': companyFlask2[4], 'companyCode': companyFlask2[5]})
    assert company2.status_code == 200
    companyList.append(companyFlask2[0])

    resp = client.post(
        '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    assert resp.status_code == 200
    userList.append(Account[0])

    add = client.post(
        '/senders/add', data={'senderName': companyFlask2[0]})
    assert add.status_code == 200

    '''
    TODO:
    '''
    create = client.post(
        '/Create', data={'senderName': companyFlask2[0]})
    assert create.status_code == 200

    send = client.post(
        '/Send', data={'senderName': companyFlask2[0]})
    assert send.status_code == 200

    extract = client.post(
        '/Extract', data={'senderName': companyFlask2[0]})
    assert send.status_code == 200
    ###############################

    remove = client.delete(
        '/senders/remove', data={'senderName': companyFlask2[0]})
    assert remove.status_code == 200
    """


def test_clear():
    clear(userList)
    clear_company(companyList)
