import pytest
from src.auth import createCompany
import random
import string
from src.clear import clear_company

companies = []


def test_create_company():
    name = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    abn = 12345678910
    street = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    suburb = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    postcode = 2000
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(10)))
    assert createCompany(name, abn, street, suburb, postcode, companycode)[
        'company_created']
    companies.append(name)


def test_create_company_duplicated_trading_name():
    name = (''.join(random.choice(string.ascii_lowercase)
                    for i in range(10)))
    abn = 12345678910
    street = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    suburb = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    postcode = 2000
    companycode = (''.join(random.choice(string.ascii_lowercase)
                   for i in range(10)))
    assert createCompany(name, abn, street, suburb, postcode, companycode)[
        'company_created']
    with pytest.raises(Exception):
        createCompany(name, abn, street, suburb, postcode, companycode)
    companies.append(name)


def test_create_company_duplicated_companycode():
    name = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
    abn = 12345678910
    street = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    suburb = (''.join(random.choice(string.ascii_lowercase)
              for i in range(10)))
    postcode = 2000
    companycode = (''.join(random.choice(string.ascii_lowercase)
                           for i in range(10)))
    assert createCompany(name, abn, street, suburb, postcode, companycode)[
        'company_created']
    with pytest.raises(Exception):
        createCompany(name, abn, street, suburb, postcode, companycode)
    companies.append(name)


def test_clear():
    clear_company(companies)
