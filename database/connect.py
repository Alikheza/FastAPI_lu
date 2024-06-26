from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , Session


engine = create_engine ("postgresql://alireza:20524219@localhost:8080/studentapp") 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session=Session(bind=engine)

def create_all_table():
    Base.metadata.create_all(bind=engine)