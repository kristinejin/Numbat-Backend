import pytest
from test.errors import DuplicateFileError
#from src.auth import Login, CreateAccount


#Account[0] = Username
#Account[1] = Passsword

#List to remove all the Accounts created
ListAccountCreated = []

#Test Account Creation
def test_account_creation(Account):
    #assert CreateAccount(Account[0],Account[1]) == True
    # ListAccountCreated.append(Account[0])
    pass

#Test Account Login
def test_login(Account):
    #assert CreateAccount(Account[0],Account[1]) == True
    # ListAccountCreated.append(Account[0])
    #assert Login(Account[0],Account[1]) == True
    pass

#Test wrong Password
def test_wrong_Password(Account,Account2):
    #assert CreateAccount(Account[0],Account[1]) == True
    # ListAccountCreated.append(Account[0])
    # with pytest.raises(WrongPassword) as e:
    #   Login(Account[0],Account2[1])
    pass

#Test invalid username/password
def test_invalid_username(invalidAccount):
    
    # with pytest.raises(InputError) as e:
    #   CreateAccount(invalidAccount[0],invalidAccount[1])
    pass

#Duplicate Username
def test_duplicate_username(Account):

    # assert CreateAccount(Account[0],Account[1]) == True
    # ListAccountCreated.append(Account[0])
    # with pytest.raises(DuplicateFileError) as e:
    #     CreateAccount(Account[0],Account[1])
    pass

#clear(ListAccountCreated)