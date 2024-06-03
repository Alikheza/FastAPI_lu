from sqlalchemy.orm import Session 
from database import module
from database.connect import engine

session=Session(bind=engine)

def create_course(db,course):
    db_course= module.course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
    

def read_course(db,id:int):
    # print(db.query(module.course).filter(module.course.course_id==id).first())
    return db.query(module.course).filter(module.course.course_id==id).first()

