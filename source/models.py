from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint, Date, DateTime
from sqlalchemy.orm import relationship, declarative_base, scoped_session, sessionmaker
from datetime import date
#from init_db import * import circulaire!

#code issu de init car probleme engine non reconnu:
# db_path = 'sqlite:///bank.db' #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier
# engine = create_engine(db_path)

Base = declarative_base() 

#DEFINIR LOGIQUE APP

class Account(Base):

    __tablename__ = "accounts"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    solde = Column(Integer)

    transactions = relationship("Transaction", back_populates='account') #la table account reference account dans la table transaction

    def __init__(self, name):
        self.name = name
        self.solde = 0

    def get_balance(self):
        return f"Votre solde actuel est: {self.solde} Deniers."
    
    def deposit(self, montant, session):
        self.montant = montant
        self.solde += montant
        new_transaction = Transaction(account=self, montant=montant, date_operation= date.today(), type_operation = 'deposit')         
        session.add(new_transaction)
        session.commit()
    
    def withdraw (self, montant, session):
        self.montant = montant
        if self.solde > montant:
            self.solde -= montant
            new_transaction = Transaction(account=self, montant=montant, date_operation=date.today(), type_operation= 'withdraw')
            session.add(new_transaction)
            session.commit()
            return self.solde
        else:
            return f'Solde insuffisant'
        
    def transfer (self, montant, receiver_account):
        self.montant = montant
        self.receiver_account = Account(receiver_account, session=session)
        return self.withdraw(montant, session), receiver_account.deposit(montant, session)
        


class Transaction(Base):

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    montant = Column(Integer) 
    date_operation = Column(DateTime)
    type_operation = Column(String)
    account = relationship('Account', back_populates='transactions')


    def __init__(self, account, montant, date_operation, type_operation):
        self.account = account
        self.montant = montant
        self.date_operation = date_operation
        self.type_operation = type_operation
      

    def __repr__(self):
        return f"Transaction enregistrée"
    

metadata = Base.metadata
if __name__ == '__main__':
    from init_db import setup_db
    session = setup_db()  # Initialiser la base de données et obtenir une session
    metadata.create_all(session.bind)
    print('%%%%%%session', session)

#test
a = Account('Tom')
a.deposit(1000, session)
a.withdraw(500)

# a = Account('Tom')

# a.deposit(1000, session)
# print('aprés dépôt', a.get_balance())
# a.withdraw(100, session)
# print('aprés retrait', a.get_balance())
# print(a.get_balance())

# d = Account('Dan')
# print('avant transfert compte recepteur d', d.get_balance())
# print('avant transfert compte emetteur', a.get_balance())

# a.transfer(500,d, session)
# print('apres transfert compte recepteur d', d.get_balance())
# print('apres transfert compte emetteur a', a.get_balance())