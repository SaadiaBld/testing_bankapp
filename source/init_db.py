from models import Base, Account, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#initialisation de la bdd

def setup_db(db_path = 'sqlite:///bank.db'): #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier

        engine = create_engine(db_path)
        try:

                Base.metadata.create_all(bind=engine)

                Session = sessionmaker(bind=engine)  #session utile pour faire ORM càd pouvoir faire des requetes sql aprés
                #session = Session()

                return Session
        
        except Exception as ex:
                print(ex)
