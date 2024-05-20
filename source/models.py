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

    def __init__(self, name, session):
        self.name = name
        self.solde = 0
        self.session = session

    def get_balance(self):
        return f"Votre solde actuel est: {self.solde} Deniers."
    
    def deposit(self, montant):
        self.montant = montant
        if self.montant > 0:
            self.solde += montant
            new_transaction = Transaction(account=self, montant=montant, date_operation= date.today(), type_operation = 'deposit')         
            self.session.add(new_transaction)
            self.session.commit()
        else:
            return f'Veuillez entrer un montant positif'
        
    def withdraw (self, montant):
        self.montant = montant
        if self.montant == 0:
            return f'Veuillez entrer un montant positif'
        elif self.montant > self.solde:
            return f'Solde insuffisant'
        else:   
            self.solde -= montant
            new_transaction = Transaction(account=self, montant=montant, date_operation=date.today(), type_operation= 'withdraw')
            self.session.add(new_transaction)
            self.session.commit()
            #return self.solde
        
    def transfer (self, montant, receiver_account):
        self.montant = montant
        self.receiver_account = Account(receiver_account, self.session)
        return self.withdraw(montant), receiver_account.deposit(montant)
        


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
    



# #test pour le terminal, mais une fois fichier example crée, mettre son code dedans
# a = Account('Tom')
# a.deposit(1000, session)
# a.withdraw(500)

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