from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from .module import ba


engine = create_engine ("postgresql://alikheza:20524219@localhost/student_system") 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_all_table():
    Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)
