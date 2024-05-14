from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime


#initialisation de la bdd
Base = declarative_base()

db_path = 'sqlite:///bank.db' #stocke chemin pr acceder a sqlite

engine = create_engine(db_path)
Session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)

#essayer la connection avec bdd
try:
        conn = engine.connect()
        print('Success')
except Exception as ex:
    print(ex)