import pytest
from src.auth import Login, CreateAccount, createCompany
from src.clear import clear, clear_company
# import psycopg2

# Account[0] = Username
# Account[1] = Passsword
# List to remove all the Accounts created
ListAccountCreated = []
ListCompanyCreated = []

# Test Account Creation


def test_account_creation(Account, company):
    assert createCompany(company['name'], company['abn'], company['street'],
                         company['suburb'], company['postcode'], company['companycode'])['company_created']
    assert CreateAccount(Account[0], Account[1],
                         company['companycode'], Account[3]) == True
    ListAccountCreated.append(Account[0])
    ListCompanyCreated.append(company['name'])


def test_account_creation_unregistered_company(Account):
    with pytest.raises(Exception):
        CreateAccount(Account[0], Account[1],
                      Account[2], Account[3])
    ListAccountCreated.append(Account[0])


# Test Account Login
def test_login(Account, company):
    assert createCompany(company['name'], company['abn'], company['street'],
                         company['suburb'], company['postcode'], company['companycode'])['company_created']
    assert CreateAccount(Account[0], Account[1],
                         company['companycode'], Account[3]) == True
    ListAccountCreated.append(Account[0])
    assert Login(Account[0], Account[1]) == True
    ListCompanyCreated.append(company['name'])


# Test wrong Password
def test_wrong_Password(Account, Account2, company):
    assert createCompany(company['name'], company['abn'], company['street'],
                         company['suburb'], company['postcode'], company['companycode'])['company_created']
    assert CreateAccount(Account[0], Account[1],
                         company['companycode'], Account[3]) == True
    ListAccountCreated.append(Account[0])
    ListCompanyCreated.append(company['name'])
    with pytest.raises(Exception):
        Login(Account[0], Account2[1])


# Test invalid username/password
def test_invalid_username(invalidAccount):

    with pytest.raises(Exception):
        CreateAccount(
            invalidAccount[0], invalidAccount[1], invalidAccount[2], invalidAccount[3]
        )


def test_repeated_username(Account, Account2, company):
    assert createCompany(company['name'], company['abn'], company['street'],
                         company['suburb'], company['postcode'], company['companycode'])['company_created']
    assert CreateAccount(Account[0], Account[1],
                         company['companycode'], Account[3]) == True
    with pytest.raises(Exception):
        CreateAccount(Account2[0], Account2[1],
                      company['companycode'], Account[3])
    ListAccountCreated.append(Account[0])
    ListCompanyCreated.append(company['name'])


def test_repeated_email(Account, Account2, company):
    assert createCompany(company['name'], company['abn'], company['street'],
                         company['suburb'], company['postcode'], company['companycode'])['company_created']
    assert CreateAccount(Account[0], Account[1],
                         company['companycode'], Account[3]) == True
    with pytest.raises(Exception):
        CreateAccount(Account2[0], Account2[1],
                      company['companycode'], Account[3])
    ListAccountCreated.append(Account[0])
    ListCompanyCreated.append(company['name'])


def test_clear():
    clear(ListAccountCreated)
    clear_company(ListCompanyCreated)
