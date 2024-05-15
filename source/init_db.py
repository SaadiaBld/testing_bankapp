from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime
from models import Base

#initialisation de la bdd

db_path = 'sqlite:///bank.db' #stocke chemin pr acceder a fichier sqlite, stocké dans le meme niveau que mon fichier

engine = create_engine(db_path)
Session = scoped_session(sessionmaker(bind=engine))  #session utile pour faire ORM càd pouvoir faire des requetes sql aprés
Session = Session()

#essayer la connection avec bdd
try:
        conn = engine.connect()
        print('Success')

        Base.metadata.create_all(bind=conn)
        Base.metadata.create_all(bind=conn)

except Exception as ex:
    print(ex)