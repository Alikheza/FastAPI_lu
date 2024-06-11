from sqlalchemy import delete , update
from sqlalchemy.orm import Session 
from database import models 
from database.connect import engine

session=Session(bind=engine)

def create_course(db,data):
    db_course= models.course(**data.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
    

def read_course(db,id):
    return db.query(models.course).filter(models.course.course_id==id).first()

def delete_course (db,id):
    query = delete(models.course).where(models.course.course_id==id)
    db.execute(query)
    db.commit()

def update_course (db,id,data):
    query = update(models.course).where(models.course.course_id==id).values(**data.dict())
    db.execute(query)
    db.commit()