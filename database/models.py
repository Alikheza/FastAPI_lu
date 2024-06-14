from .connect import Base
from sqlalchemy import Column,ForeignKey,INTEGER,VARCHAR,SMALLINT

''''''
class course (Base):
    
    __tablename__="course"
    
    course_id = Column(VARCHAR,primary_key=True)
    course_name = Column(VARCHAR)
    course_department = Column(VARCHAR)
    course_credit = Column(SMALLINT)

class Professor(Base):

    __tablename__='professor'

    user_Fname = Column(VARCHAR)
    user_Lname = Column(VARCHAR)
    user_birthday = Column(VARCHAR)
    user_ID = Column(VARCHAR,unique=True)
    user_province = Column(VARCHAR)
    user_borncity = Column(VARCHAR)
    user_address = Column(VARCHAR)
    user_postal_code = Column(VARCHAR)
    user_phone_number = Column(VARCHAR)
    user_home_number = Column(VARCHAR)
    user_department = Column(VARCHAR)
    user_major = Column(VARCHAR)
    user_professor_id=Column(VARCHAR,primary_key =True)

class Student(Base):

    __tablename__='student'

    user_Fname = Column(VARCHAR,nullable=False)
    user_Lname = Column(VARCHAR)
    user_birthday = Column(VARCHAR)
    user_ID = Column(VARCHAR ,unique=True)
    user_province = Column(VARCHAR)
    user_borncity = Column(VARCHAR)
    user_address = Column(VARCHAR)
    user_postal_code = Column(VARCHAR)
    user_phone_number = Column(VARCHAR)
    user_home_number = Column(VARCHAR) 
    user_department = Column(VARCHAR)
    user_major = Column(VARCHAR)
    user_student_number = Column(VARCHAR,primary_key=True)
    user_student_father_name = Column(VARCHAR)
    user_student_IDS = Column(VARCHAR,unique=True)
    user_student_married = Column(VARCHAR)

class Relation_table(Base):

    __tablename__ = 'course_professor_student'

    serial = Column(INTEGER,primary_key =True)
    user_student_number = Column(VARCHAR,ForeignKey('student.user_student_number', onupdate="CASCADE"))
    course_id = Column(VARCHAR,ForeignKey('course.course_id' , onupdate="CASCADE" , ondelete="CASCADE"))
    user_professor_id = Column(VARCHAR,ForeignKey('professor.user_professor_id' , onupdate="CASCADE",ondelete="CASCADE"))
