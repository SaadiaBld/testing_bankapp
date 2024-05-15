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

    transactions = relationship("Transaction", back_populates='accounts') #la table account reference account dans la table transaction

    def __init__(self, name, session):
        self.name = name
        self.solde = 0
        self.session = session

    def get_balance(self):
        return f"Votre solde actuel est: {self.solde} Couronnes."
    
    def deposit(self, montant):
        self.montant = montant
        self.solde += montant
        new_transaction = Transaction(account=self, montant=montant, date_operation= date.today(), type_operation = 'deposit')         
        self.session.add(new_transaction)
        self.session.commit()
    
    def withdraw (self, montant):
        self.montant = montant
        if self.solde > montant:
            self.solde -= montant
            new_transaction = Transaction(account=self, montant=montant, date_operation=date.today(), type_operation= 'withdraw')
            self.session.add(new_transaction)
            self.session.commit()
            return self.solde
        else:
            return f'Solde insuffisant'
        
    def transfer (self, montant, receiver_account):
        self.montant = montant
        self.receiver_account = Account(receiver_account, session=self.session)
        return self.withdraw(self.montant), receiver_account.deposit(self.montant)
        


class Transaction(Base):

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    montant = Column(Integer) 
    date_operation = Column(DateTime)
    type_operation = Column(String)
    accounts = relationship('Account', back_populates='transactions')


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
    Session = setup_db()  # Initialiser la base de données et obtenir une session
    session = Session()
    metadata.create_all(engine)

#test
a = Account('Tom', 2)
a.deposit(1000)
print('aprés dépôt', a.solde)
a.withdraw(100)
print('aprés retrait', a.solde)
print(a.get_balance())

d = Account('Dan')
print('avant transfert compte recepteur d', d.get_balance())
print('avant transfert compte emetteur', a.get_balance())

a.transfer(500,d)
print('apres transfert compte recepteur d', d.get_balance())
print('apres transfert compte emetteur a', a.get_balance())