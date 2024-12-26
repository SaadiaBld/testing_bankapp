from source.models import Base, Account, Transaction
from sqlalchemy import create_engine #sert à créer une connexion avec une bdd spécidique ((ici, SQLite via 'sqlite:///bank.db'))
from sqlalchemy.orm import sessionmaker #configurer session pour interagir avec bdd

#initialisation de la bdd

def setup_db(db_path = 'sqlite:///bank.db'): #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier
        '''configurer et initialiser la bdd'''
        engine = create_engine(db_path)  #configurer connexion à bdd, engine sert à executer les commandes sql et gerer interactions avec base
        Base.metadata.create_all(engine)  #creer les tables dans bdd sur base de modeles definis dans models.py
        Session = sessionmaker(bind=engine) #session pour 
        return Session()
      
