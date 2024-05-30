from .connect import Base
from sqlalchemy import  Column, Integer, String ,VARCHAR

class course (Base):
    
    __tablename__="course"
    course_id = Column(VARCHAR,primary_key=True)
    course_name = Column(VARCHAR)
    course_department = Column(VARCHAR)
    course_credit = Column(Integer)