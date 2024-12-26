import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from source.models import Transaction, Account
from source.init_db import setup_db
from sqlalchemy.orm import Session
from mock_alchemy.mocking import AlchemyMagicMock

Base = declarative_base()
#https://coderpad.io/blog/development/a-guide-to-database-unit-testing-with-pytest-and-sqlalchemy/
# @pytest.fixture
# def test_session(db): #fixture fournit une bdd temporaire pour chaque test
#     return db.session

# @pytest.fixture
# def test_account(name, test_session):
#     return Account(name = name)
   

# def test_deposit(test_account):
#     test_deposit = Account.deposit(amount = 1000)
#     test_account.session.add(test_deposit)
#     test_account.session.commit()
    
#     #test de deposit
#     account_x = test_account.name('test')
#     assert account_x.name == 'test'
#     assert account_x.amount == 1000

###############
@pytest.fixture
def db_session():
    engine = create_engine()
    Base.metadata.create_all(engine)
    session = Session(AlchemyMagicMock())
    yield session
    session.rollback()
    session.close()

# @pytest.fixture(scope='module')
# def valid_account():
#     valid_account = Account(name = "Flash", session= db_session())
#     return valid_account

@pytest.fixture
class TestBank:
    def test_account_valid(self, valid_account, db_session):
        db_session.add(valid_account)
        db_session.commit()
        flash = db_session.query(Account)
        assert flash.name == 'Flash'
        assert flash.solde == 0
        
    def test_deposit():
        if montant <= 0:
            raise ValueError("Le montant du dépôt doit être positif.")
            self.solde += montant
        pass
        
        # Base.metadata.create_all(engine)
        # self.session = Session()
        # self.valid_account = Account(
        #     name = "Dr Strange",
        #     session = self.session)
        