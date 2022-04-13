import pytest
from src.auth import Login, CreateAccount
from src.clear import clear
# import psycopg2

# Account[0] = Username
# Account[1] = Passsword
# List to remove all the Accounts created
ListAccountCreated = []

# Test Account Creation


def test_account_creation(Account):
    assert CreateAccount(Account[0], Account[1],
                         Account[2], Account[3]) == True
    ListAccountCreated.append(Account[0])


# Test Account Login
def test_login(Account):
    assert CreateAccount(Account[0], Account[1],
                         Account[2], Account[3]) == True
    ListAccountCreated.append(Account[0])
    assert Login(Account[0], Account[1]) == True


# Test wrong Password
def test_wrong_Password(Account, Account2):
    assert CreateAccount(Account[0], Account[1],
                         Account[2], Account[3]) == True
    ListAccountCreated.append(Account[0])
    with pytest.raises(Exception):
        Login(Account[0], Account2[1])


# Test invalid username/password
def test_invalid_username(invalidAccount):

    with pytest.raises(Exception):
        CreateAccount(
            invalidAccount[0], invalidAccount[1], invalidAccount[2], invalidAccount[3]
        )


def test_repeated_username(Account, Account2):
    assert CreateAccount(Account[0], Account[1],
                         Account[2], Account[3]) == True
    # with pytest.raises(Exception):
    CreateAccount(Account2[0], Account2[1], Account2[2], Account[3])
    ListAccountCreated.append(Account[0])


def test_repeated_email(Account, Account2):
    assert CreateAccount(Account[0], Account[1],
                         Account[2], Account[3]) == True
    # with pytest.raises(Exception):
    CreateAccount(Account2[0], Account2[1], Account2[2], Account[3])
    ListAccountCreated.append(Account[0])


def test_clear():
    clear(ListAccountCreated)
