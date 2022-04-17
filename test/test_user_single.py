import pytest
from src.FlaskApp import app
from src.clear import clear, clear_company
import json
from src.select_all import selectAll

@pytest.fixture
def client():
    return app.test_client()

# def test_Test_route(client, Account, companyFlask):
#     company = client.post('/create/company', data={'name': companyFlask[0], 'abn': companyFlask[1], 'street': companyFlask[2],
#                                                    'suburb': companyFlask[3], 'postcode': companyFlask[4], 'companyCode': companyFlask[5]})
#     assert company.status_code == 200
#     resp = client.post(
#         '/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': companyFlask[5], 'Email': Account[3]})
    
#     print('UserName: ' + Account[0] + '   Password: ' + Account[1] + '   CompanyCode: ' + companyFlask[5] + '   Email: ' + Account[3])

#     resp = client.post('/Test', json={})
#     print("SERVER RESPONSES")
#     print(resp.data.decode("utf-8"))
#     assert 10 == 5
    
# def test_Home_route(client):
#     # resp = client.post(
#     #     '/UserLogin', data={'UserName': 'alpha', 'Password': 'beta'})
#     resp = client.post(
#         '/UserLogin', data={'UserName': 'alpha', 'Password': 'beta'})
#     assert resp.status_code == 200
#     resp = client.post(
#         '/Home', data={})
#     assert resp.status_code == 200
#     print(resp.data.decode("utf-8"))
#     assert 10 == 5

# results = selectAll("a")
# print(results)
    