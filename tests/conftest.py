import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source.models import Account, Transaction


# # Fixture pour une session mock de la base de données
# @pytest.fixture(scope="function")
# def mock_session(): 
#     engine = create_engine('sqlite:///:memory:')  # Utilise une base de données SQLite en mémoire
#     Session = sessionmaker(bind=engine)
#     session =UnifiedAlchemyMagicMock()
#     yield session
#     session.rollback()
#     #return session

# @pytest.fixture
# def test_account(mock_session):
#     return Account(name="Test Account", session=mock_session)

# @pytest.fixture
# def test_deposit(test_account):
#     test_account.deposit(1000)
#     return test_account

session = UnifiedAlchemyMagicMock()
session.add(Account(name='Batman', session=session))
session.query(Account).filter_by(id=1).first().name
