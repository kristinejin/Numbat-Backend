import pytest
import random
import string

@pytest.fixture
def Account():
    Username = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    Password = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    return(Username,Password)

@pytest.fixture
def Account2():
    Username = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    Password = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    return(Username,Password)

@pytest.fixture
def invalidAccount():
    Username = ''.join((random.choice(string.ascii_letters) for x in range(7)))  
    Username += ''.join((random.choice(string.digits) for x in range(7)))

    Password = ''.join((random.choice(string.ascii_letters) for x in range(7)))  
    Password += ''.join((random.choice(string.digits) for x in range(7)))  
    return(Username,Password)