from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session
from config import Evariable

SQLALCHEMY_DATABASE_URL = f'postgresql://{Evariable.DATABASE_USERNAME}:{Evariable.DATABASE_PASSWORD}@{Evariable.DATABASE_HOST}:{Evariable.DATABASE_PORT}/{Evariable.DATABASE_NAME}'

print(SQLALCHEMY_DATABASE_URL)
engine = create_engine (SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session=Session(bind=engine)

def create_all_table():
    Base.metadata.create_all(bind=engine)