import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from source.models import Transaction, Account, Base

# Fixture pour configurer une base en mémoire pour chaque test
@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')  # Base temporaire en mémoire
    Base.metadata.create_all(engine)  # Créer les tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Fournit la session au test
    session.rollback()  # Annule les changements après chaque test
    session.close()

# Fixture pour créer un compte valide
@pytest.fixture
def valid_account(db_session):
    account = Account(name="Flash", session=db_session)
    db_session.add(account)
    db_session.commit()
    return account

# Classe pour les tests
class TestBank:
    def test_account_valid(self, valid_account, db_session):
        #vérifie que le compte a été créé avec le solde initial correct
        flash = db_session.query(Account).filter_by(name="Flash").first()
        assert flash.name == 'Flash'
        assert flash.solde == 0

    def test_deposit(self, valid_account, db_session):
        # Effectue un dépôt et vérifie le nouveau solde
        valid_account.deposit(1000)
        assert valid_account.solde == 1000

    
    def test_deposit_creates_transaction(self, valid_account, db_session):
        # Effectue un dépôt et vérifie qu'une transaction est créée
        valid_account.deposit(1000)

        # Vérifier qu'une transaction a bien été enregistrée
        transactions = db_session.query(Transaction).filter_by(account_id=valid_account.id).all()
        assert len(transactions) == 1

        # Vérifier les détails de la transaction
        transaction = transactions[0]
        assert transaction.montant == 1000
        assert transaction.type_operation == 'deposit'

    def test_deposit_invalid_amount(self, valid_account):
        # Tenter un dépôt avec un montant négatif
        with pytest.raises(ValueError, match="Le montant du dépôt doit être positif."):
            valid_account.deposit(-500)

        # Vérifier que le solde n'a pas changé
        assert valid_account.solde == 0

    def test_transfer_normal(self, db_session):
        #2 comptes crées pour transfert
        sender = Account(name="Sender", session=db_session)
        receiver = Account(name="Receiver", session=db_session)
        db_session.add(sender)
        db_session.add(receiver)
        db_session.commit()

        #fonds ajoutés sur compte emetteur
        sender.deposit(1000)

        # realiser un transfert
        sender.transfer(500, receiver)

        # verifie les soldes des comptes
        assert sender.solde == 500
        assert receiver.solde == 500

        # vérifier les transactions
        sender_transaction = db_session.query(Transaction).filter_by(account_id=sender.id, type_operation="withdraw").first()
        receiver_transaction = db_session.query(Transaction).filter_by(account_id=receiver.id, type_operation="deposit").first()

        assert sender_transaction is not None
        assert sender_transaction.montant == 500
        assert receiver_transaction is not None
        assert receiver_transaction.montant == 500