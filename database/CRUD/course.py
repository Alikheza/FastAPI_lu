from sqlalchemy import  update
from database import models 

def create_course(db,data):
    db_course= models.course(**data.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
    

def read_course(db,id):
    return db.query(models.course).filter(models.course.course_id==id).first()

def delete_course (db,id):
    query = db.query(models.course).where(models.course.course_id==id).first()
    delete = models.association_table.delete().where(models.association_table.c.course_id==id)
    db.delete(query)
    db.execute(delete)
    db.commit()

def update_course (db,id,data):
    relation = models.association_table.update().where(models.association_table.c.course_id==id).values(course_id=data.course_id)
    query = update(models.course).where(models.course.course_id==id).values(**data.dict())
    db.execute(relation)
    db.execute(query)
    db.commit()