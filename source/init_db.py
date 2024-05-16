from source.models import Base, Account, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#initialisation de la bdd

def setup_db(db_path = 'sqlite:///bank.db'): #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()
      
