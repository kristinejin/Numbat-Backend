import pytest
from test.errors import DuplicateFileError, WrongPassword
from src.auth import Login, CreateAccount
from src.clear import clear
import psycopg2
#Account[0] = Username
#Account[1] = Passsword
#List to remove all the Accounts created
ListAccountCreated = []

#Test Account Creation
def test_account_creation(Account):
	assert CreateAccount(Account[0],Account[1]) == True
	ListAccountCreated.append(Account[0])

#Test Account Login
def test_login(Account):
	assert CreateAccount(Account[0],Account[1]) == True
	ListAccountCreated.append(Account[0])
	assert Login(Account[0],Account[1]) == True
	

#Test wrong Password
def test_wrong_Password(Account,Account2):
	assert CreateAccount(Account[0],Account[1]) == True
	ListAccountCreated.append(Account[0])
	with pytest.raises(Exception) as e:
	  Login(Account[0],Account2[1])
	

#Test invalid username/password
def test_invalid_username(invalidAccount):
	
	with pytest.raises(Exception) as e:
	  CreateAccount(invalidAccount[0],invalidAccount[1])
	

#Duplicate Username
def test_duplicate_username(Account):

	assert CreateAccount(Account[0],Account[1]) == True
	ListAccountCreated.append(Account[0])
	with pytest.raises(psycopg2.errors.UniqueViolation) as e:
		CreateAccount(Account[0],Account[1])

def test_clear():
	clear(ListAccountCreated)	
