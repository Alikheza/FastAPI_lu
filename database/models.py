from .connect import Base
from sqlalchemy import Column,ForeignKey,INTEGER,VARCHAR,SMALLINT ,Table
from sqlalchemy.orm import relationship

association_table = Table(
    'association',
    Base.metadata,
    Column('course_id', VARCHAR, ForeignKey('course.course_id', ondelete='CASCADE', onupdate='CASCADE')),
    Column('user_professor_id', VARCHAR, ForeignKey('professor.user_professor_id', ondelete='CASCADE', onupdate='CASCADE')),
    Column('user_student_number', VARCHAR, ForeignKey('student.user_student_number', ondelete='CASCADE', onupdate='CASCADE'))

)

class course(Base):
    __tablename__ = "course"

    course_id = Column(VARCHAR, primary_key=True)
    course_name = Column(VARCHAR)
    course_department = Column(VARCHAR)
    course_credit = Column(SMALLINT)

    students = relationship("Student", secondary=association_table, back_populates="courses")
    professors = relationship("Professor", secondary=association_table, back_populates="courses" ,overlaps="students")

class Professor(Base):
    __tablename__ = 'professor'

    user_Fname = Column(VARCHAR)
    user_Lname = Column(VARCHAR)
    user_birthday = Column(VARCHAR)
    user_ID = Column(VARCHAR, unique=True)
    user_province = Column(VARCHAR)
    user_borncity = Column(VARCHAR)
    user_address = Column(VARCHAR)
    user_postal_code = Column(VARCHAR)
    user_phone_number = Column(VARCHAR)
    user_home_number = Column(VARCHAR)
    user_department = Column(VARCHAR)
    user_major = Column(VARCHAR)
    user_professor_id = Column(VARCHAR, primary_key=True)

    courses = relationship("course", secondary=association_table, back_populates="professors",overlaps="students")
class Student(Base):
    __tablename__ = 'student'

    user_Fname = Column(VARCHAR)
    user_Lname = Column(VARCHAR)
    user_birthday = Column(VARCHAR)
    user_ID = Column(VARCHAR, unique=True)
    user_province = Column(VARCHAR)
    user_borncity = Column(VARCHAR)
    user_address = Column(VARCHAR)
    user_postal_code = Column(VARCHAR)
    user_phone_number = Column(VARCHAR)
    user_home_number = Column(VARCHAR)
    user_department = Column(VARCHAR)
    user_major = Column(VARCHAR)
    user_student_number = Column(VARCHAR, primary_key=True)
    user_student_father_name = Column(VARCHAR)
    user_student_IDS = Column(VARCHAR, unique=True)
    user_student_married = Column(VARCHAR)

    courses = relationship("course", secondary=association_table, back_populates="students",overlaps="courses,professors")


class Admin(Base):
    __tablename__ = 'admin'

    user_name = Column(VARCHAR)
    user_admin_id = Column(INTEGER, primary_key=True)