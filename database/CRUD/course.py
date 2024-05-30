from sqlalchemy.orm import Session 
from database import course_module
from database.connect import engine
# from shcemas.course import Course_Info_In , Course_Info_Out

session=Session(bind=engine)

def create_course(db,course):
    db_course= course_module.course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
    

def read_course(db,id:int):
    return db.query(course_module.course).filter(course_module.course.course_id==id).first()

