import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from source.models import Base, Account, Transaction
from source.init_db import setup_db
from sqlalchemy.orm import Session, sessionmaker
from alchemy_mock.mocking import UnifiedAlchemyMagicMock


@pytest.fixture(scope="function")
def mock_session(): #fixture fournit une bdd temporaire pour chaque test, utilise alchemy_mock pour simuler une session sqlalchemy  
    engine = create_engine('sqlite:///:memory:') #créer un nouvel engine pour 1 bdd locale sqlite en memoire (pas de fichier) 
    #Session = sessionmaker(bind=engine) #créer une session
    mock_session = UnifiedAlchemyMagicMock() #mock_session est une instance de UnifiedAlchemyMagicMock
    return mock_session

## test deposit normal
def test_deposit(mock_session):
    account = Account(name = "Test_Batman", session=mock_session)
    account.deposit(1000)

    mock_session.add.assert_called() #vérifie que mock_session.add a été appelé
    mock_session.commit.assert_called() #idem pour mock_session.commit
   
def test_deposit_high(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)

    mock_session.add.assert_called() #vérifie que mock_session.add a été appelé
    mock_session.commit.assert_called() #idem pour mock_session.commit

def test_solde(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    account.withdraw(1000)
    assert account.solde == 4000

def test_transaction_is_deposit(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).first()
    assert transaction.type_operation == 'deposit'

def test_timestamp_registered(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).first()
    assert transaction.date_operation.strftime('%Y-%m-%d') == '2024-05-20' #methode strftime convertit date en string

def test_session_commit(mock_session):
    account = Account(name='Coco', session=mock_session)
    account.deposit(100)
    mock_session.commit.assert_called_once() #vérifie que mock_session.commit a été appelé

## test_deposit_negative_amount
def test_deposit_negative_amount(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(-5000)
    assert account.solde == 0

def test_deposit_negative_amount_no_transaction(mock_session):  
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(-5000)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).first()
    assert transaction == None

def test_deposit_negative_amount_no_session_commit(mock_session):   
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(-5000)
    mock_session.commit.assert_not_called()


    
## test_deposit_zero_amount
def test_deposit_null_amount_no_transaction(mock_session):
    account=Account(name="Test_Wolverine", session=mock_session)
    account.deposit(0)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).first() #recupere une transaction pour le compte à partir de la bdd, si aucune transaction, renvoie None
    assert transaction == None

def test_deposit_null_amount(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(0)
    assert account.solde == 0

def test_deposit_null_amount_no_session_commit(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(0)
    mock_session.commit.assert_not_called() #vérifie que mock_session.commit n'a pas été appelé

def test_solde_equal_deposit_null(mock_session):
    account = Account(name = "Test_Wolverine",session=mock_session)
    account.deposit(0)
    assert account.solde == 0

## test_withdraw_normal
def test_withdraw_normal(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    account.withdraw(1000)
    assert account.solde == 4000

def test_withdraw_transaction_registered(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    account.withdraw(1000)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).all()
    assert transaction[1].type_operation == 'withdraw'

def test_withdraw_insuficient_funds(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.deposit(5000)
    account.withdraw(10000)
    assert account.solde == 5000

def test_withdraw_insuficient_funds_no_transaction(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.withdraw(1000)
    transaction = mock_session.query(Transaction).filter_by(account_id=1).first()
    assert transaction == None

def test_withdraw_no_session_commit(mock_session):
    account = Account(name = "Test_Wolverine", session=mock_session)
    account.withdraw(1000)
    mock_session.commit.assert_not_called()
    
