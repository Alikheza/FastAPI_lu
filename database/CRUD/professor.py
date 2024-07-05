from sqlalchemy import delete , update
from database import models 
from fastapi import HTTPException


# functions for create professor and corse relationship 
def create_professor(db,data):
    db_pro=models.Professor(**data.dict(exclude={'user_professor_course_IDs'}))
    db.add(db_pro)
    try:
        check_relation = db.query(models.association_table).filter(models.association_table.c.course_id.in_(data.user_professor_course_IDs.split('-'))).all()
        for i in check_relation:raise ValueError(f' درس{i.course_id} قبلا به استاد دیگری داده شده است')
        db.commit()
        professor_R(db=db, data=data)
    except Exception as e:
        raise HTTPException(detail=f"{e!r}مشکلی در ثبت اطلاعات استاد به وجود امده است لطفا مقادیر وارده شده را دوباره چک کنید",status_code=400)
def professor_R(db, data):
    professor = read_professor(db=db, p_id=data.user_professor_id)
    course= db.query(models.course).filter(models.course.course_id.in_(data.user_professor_course_IDs.split('-'))).all()
    professor.courses.extend(i for i in course)
    db.commit()



#functions for read professor and professor_corse_relationship 
def read_professor(db,p_id):
    return db.query(models.Professor).filter(models.Professor.user_professor_id==p_id).first()

def read_relationship_CR(db, id_p, id_c, _not_=False):
    query = db.query(models.association_table).filter(models.association_table.c.course_id == id_c)
    if _not_:
        query = query.filter(models.association_table.c.user_professor_id != id_p)
    else:
        query = query.filter(models.association_table.c.user_professor_id == id_p)
    return query.first()


#function for delete professor
def delete_professor(db, id):
    professor = db.query(models.Professor).filter(models.Professor.user_professor_id == id).first()
    delete = models.association_table.delete().where(models.association_table.c.user_professor_id==id)
    db.delete(professor)
    db.execute(delete)
    db.commit()




#functions for updating professor (use select function ,so the user should not send all the data again)
def update_professor(db, data, id):
    query = update(models.Professor).where(models.Professor.user_professor_id == id).values(**data.dict(exclude={'user_professor_course_IDs'}))
    db.execute(query)
    relation = models.association_table.update().where(models.association_table.c.user_professor_id==id).values(user_professor_id = data.user_professor_id)
    db.execute(relation)
    db.commit()

def select_professor(db , id):
    results = (
        db.query(models.Professor, models.association_table.c.course_id)
        .outerjoin(models.association_table, models.Professor.user_professor_id == models.association_table.c.user_professor_id)
        .filter(models.Professor.user_professor_id == id)
        .all()
    )
    professor_data = {}
    user_professor_course_IDs = []
    for result in results:
        professor, course_id = result
        if not professor_data:
            professor_data = {
                "user_ID": str(professor.user_ID),
                "user_Fname": professor.user_Fname,
                "user_province": professor.user_province,
                "user_address": professor.user_address,
                "user_phone_number": str(professor.user_phone_number),
                "user_department": professor.user_department,
                "user_professor_id": professor.user_professor_id,
                "user_Lname": professor.user_Lname,
                "user_birthday": professor.user_birthday,
                "user_borncity": professor.user_borncity,
                "user_postal_code": str(professor.user_postal_code),
                "user_home_number": str(professor.user_home_number),
                "user_major": professor.user_major
            }
        if course_id:
            if course_id not in user_professor_course_IDs:
                user_professor_course_IDs.append(course_id)
    formatstr = '-'.join(user_professor_course_IDs)
    professor_data['user_professor_course_IDs']=formatstr 
    return professor_data

