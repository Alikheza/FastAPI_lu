from sqlalchemy import delete , update
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
    

def read_course(db,id):
    return db.query(module.course).filter(module.course.course_id==id).first()

def delete_course (db,id):
    query = delete(module.Relation_table).where(module.Relation_table.course_id==id)
    db.execute(query)
    query = delete(module.course).where(module.course.course_id==id)
    db.execute(query)
    db.commit()

def update_course (db,id,data):
    if id == data.course_id :
        query = update(module.course).where(module.course.course_id==id).values(**data.dict())
        db.execute(query)
        db.commit()
    else :
        create_course(db,course=data)
        query = update(module.Relation_table).where(module.Relation_table.course_id==id).values(course_id=(data.course_id))
        db.execute(query)
        query = delete(module.course).where(module.course.course_id==id)
        db.execute(query)
        db.commit()