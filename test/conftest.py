import pytest
import random
import string


@pytest.fixture
def Account():
    Username = (''.join(random.choice(string.ascii_lowercase)
                for i in range(10)))
    Password = (''.join(random.choice(string.ascii_lowercase)
                for i in range(10)))
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(10)))
    email = (''.join(random.choice(string.ascii_lowercase)
             for i in range(10))) + "@test.com"
    return(Username, Password, companycode, email)


@pytest.fixture
def Account2():
    Username = (''.join(random.choice(string.ascii_lowercase)
                for i in range(10)))
    Password = (''.join(random.choice(string.ascii_lowercase)
                for i in range(10)))
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(10)))
    email = (''.join(random.choice(string.ascii_lowercase)
             for i in range(15))) + "@test.com"
    return(Username, Password, companycode, email)


@pytest.fixture
def invalidAccount():
    Username = ''.join((random.choice(string.ascii_letters) for x in range(7)))
    Username += ''.join((random.choice(string.digits) for x in range(7)))

    Password = ''.join((random.choice(string.ascii_letters) for x in range(7)))
    Password += ''.join((random.choice(string.digits) for x in range(7)))

    companycode = ''.join((random.choice(string.ascii_letters)
                          for x in range(7)))

    email = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))

    return(Username, Password, companycode, email)


@pytest.fixture
def company():
    name = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    abn = 12345678910
    street = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
    suburb = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
    postcode = 2000
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(5)))
    company_det = {
        "name": name,
        "abn": abn,
        "street": street,
        "suburb": suburb,
        "postcode": postcode,
        "companycode": companycode
    }
    return company_det


@pytest.fixture
def companyFlask():
    name = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    abn = 12345678910
    street = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
    suburb = (''.join(random.choice(string.ascii_lowercase) for i in range(5)))
    postcode = 2000
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(5)))
    return(name, abn, street, suburb, postcode, companycode)
