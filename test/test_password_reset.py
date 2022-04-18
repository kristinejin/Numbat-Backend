# import pytest
# import random
# import string
# from src.FlaskApp import app
# from src.clear import clear
# from test.xml_str import xml_as_string
# from src.other import checkUniqueEmail

# @pytest.fixture
# def client():
#     return app.test_client()


# def test_register_anonymous(client,Account):
#     resp = client.get('/Register')
#     assert resp.status_code == 200
#     resp = client.post('/Register', data={'UserName': Account[0], 'Password': Account[1], 'CompanyCode': Account[2], 'Email': Account[3]})
#     assert resp.status_code == 302
#     resp = client.post('/Logout', data={'Logout': 'Logout'})
#     assert resp.status_code == 302
    
#     Filename = (''.join(random.choice(string.ascii_lowercase)
#                 for i in range(9)))
#     print("Username: " + Account[0] + "   Password: " + Account[1] + "   Filename: " + Filename + "   Companycode: " + Account[2] + "   Email: " + Account[3])
#     resp = client.post(
#         '/Store', data={'FileName': Filename, 'Password': Account[2], 'XML': xml_as_string})
#     print(resp.data)
#     print(resp.text)
#     assert 10 == 5

# def test_register(client):

#     resp = client.get('/Register')
#     assert resp.status_code == 200
#     resp = client.post('/Register', data={'UserName': 'passreset', 'Password': 'password', 'CompanyCode': '1234', 'Email': 'matthew.druckman@gmail.com'})
#     assert resp.status_code == 302
#     resp = client.post('/Logout', data={'Logout': 'Logout'})
#     assert resp.status_code == 302
#     resp = client.post('/passwordreset/request', json={"email": "matthew.druckman@gmail.com"})
#     print(resp.json()["reset_code_status"])
#     assert 10 == 2

# def test_reset_code_sent(client):

#     resp = client.post('/passwordreset/request', json={"email": "matthew.druckman@gmail.com"})
#     print(resp.json()["reset_code_status"])
#     print(resp.status_code)
#     assert 10 == 2

# def test_reset_code_works(client):
#     resp = client.post('/passwordreset/reset', json={"reset_code": "36810", "new_password": "new_pass"})
#     print(resp.text)
#     print(resp.data)
#     assert 10 == 2

# email = "matthew.druckman@gmail.com"
# solution = checkUniqueEmail(email)
# print(solution)
    