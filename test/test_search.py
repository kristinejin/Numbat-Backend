from test.xml_str_for_search import generate_random_date, generate_random_name, generate_unique_xml
import pytest
from src.FlaskApp import app
# from test.xml_str import xml_as_string
# from src.check_num_render_or_store import checkQuota
# import random
# import string


@pytest.fixture
def client():
    return app.test_client()


def store_helper():
    date = generate_random_date()
    sender_name = generate_random_name(60)
    xml = generate_unique_xml(date, sender_name)
    xml_name = generate_random_name(10)
    return {
        'issue_date': date,
        'sender_name': sender_name,
        'xml': xml,
        'xml_name': xml_name
    }

# def test_search_both(Account, client):
#     invoice_info = store_helper()
#     Filename = (''.join(random.choice(string.ascii_lowercase)
#                 for i in range(9)))
#     resp = client.post(
#         '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
#     assert resp.status_code == 302
#     resp = client.post(
#         '/Store', data={'FileName': Filename, 'XML': invoice_info["xml"]})
#     assert resp.status_code == 200
#     resp = client.post('/Search', data={'issue_date': invoice_info['issue_date'], 'sender_name': invoice_info['sender_name']})
#     # print(Filename + " + " + invoice_info['issue_date'] + " + " + invoice_info['sender_name'])
#     # print(resp)
#     # print(resp.status_code)
#     # print(resp.text)
#     assert 10 == 5


# def test_search_name(Account, client):
#     invoice_info = store_helper()
#     Filename = (''.join(random.choice(string.ascii_lowercase)
#                 for i in range(9)))
#     resp = client.post(
#         '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
#     assert resp.status_code == 302
#     resp = client.post(
#         '/Store', data={'FileName': Filename, 'XML': invoice_info["xml"]})
#     assert resp.status_code == 200
#     resp = client.post('/Search', data={'issue_date': invoice_info['issue_date'], 'sender_name': ''})

#     assert 10 == 5

# def test_search_name(Account, client):
#     invoice_info = store_helper()
#     Filename = (''.join(random.choice(string.ascii_lowercase)
#                 for i in range(9)))
#     resp = client.post(
#         '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
#     assert resp.status_code == 302
#     resp = client.post(
#         '/Store', data={'FileName': Filename, 'XML': invoice_info["xml"]})
#     assert resp.status_code == 200
#     resp = client.post('/Search', data={'issue_date': '', 'sender_name': invoice_info["sender_name"]})
#     print(Filename + " + " + invoice_info['issue_date'] + " + " + invoice_info['sender_name'])
#     # print(resp)
#     # print(resp.status_code)
#     # print(resp.text)
#     assert 10 == 5
