#brief = definir classes account et transactions. account communique le solde, transactions 
#example.app est un fichier qui va simuler l'app (remplace le django ou autre)
#sqlachemy va avoir effet sur bdd, donc example.app va creer entrees pour la bdd. L'idee est de tester le mocking en simulant la bdd pour qu moment du test de ne pas polluer la bdd
#avec sqlachemy, la classe est le reflet de la bdd
#transfert = sortie d'un compte A et entree dans un compte B
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base, scoped_session, sessionmaker

#code issu de init car probleme engine non reconnu:
db_path = 'sqlite:///bank.db' #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier
engine = create_engine(db_path)

Base = declarative_base() 


#DEFINIR LOGIQUE APP

class Account(Base):

    __tablename__ = "accounts"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    solde = Column(Integer)

    transactions = relationship("Transaction", back_populates='accounts') #la table account reference account dans la table transaction

    def __init__(self, name):
        self.name = name
        self.solde = 0
    
    def __repr__(self):
        return f"Compte crée au nom de {self.name}. Votre solde initial est {self.solde}"
    
    # def get_balance(self):
    #     new_transaction = Transaction(account = self, montant = self.montant)
    #     session = Session()
    #     session.add(new_transaction)
    #     session.commit()
    #     print('Voici l\'id de la new_transaction:', new_transaction.id)



class Transaction(Base):

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    montant = Column(Integer) 
    accounts = relationship('Account', back_populates='transactions')


    def __init__(self, account, montant):
        self.account = account
        self.montant = montant
      

    # def __repr__(self):
    #     return f"Transaction enregistrée"
    
    # def deposit (self, amount):
    #     self.amount = amount
    #     self.solde += amount
    #     return self.solde

    # def withdraw (self, amount):
    #     self.account -= amount
    #     return self.account 

    # def transfer (self, amount, destination_account):
    #     self.destination_account += self.amount


metadata = Base.metadata
if __name__ == '__main__':
    metadata.create_all(engine)
#Base.metadata.create_all(engine) 
a = Account('Tom')
