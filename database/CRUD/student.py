from database import models
from sqlalchemy import  update 
from fastapi import HTTPException
    
def create_student_db (db, data):
    try : 
        db_S = models.Student(**data.dict(exclude={'course_professor_IDL'}))
        db.add(db_S)
        db.commit()
        db.refresh(db_S)
    except Exception as e :
        raise HTTPException(detail=f"{e!r}مشکلی در ثبت اطلاعات استاد به وجود امده است لطفا مقادیر وارده شده را دوباره چک کنید",status_code=400)
    student_R(db , data)
  
def student_R (db,data):
    course_professor_IDL = eval(data.course_professor_IDL)
    for professor_ids , course_ids in course_professor_IDL.items():
        for course_id in course_ids:
            relation = models.association_table.insert().values(user_student_number=data.user_student_number, course_id=course_id, user_professor_id=professor_ids)
            delete = models.association_table.delete().where(models.association_table.c.course_id==course_id, models.association_table.c.user_professor_id==professor_ids , models.association_table.c.user_student_number==None)
            db.execute(relation)
            db.execute(delete)
    db.commit()

def read_student_ID (db,s_id:str):
    return db.query(models.Student).filter(models.Student.user_student_number==s_id).first()


def delete_student (db , s_id ):
    query=read_student_ID(db, s_id)
    db.delete(query)
    delete = models.association_table.delete().where(models.association_table.c.user_student_number==s_id)
    db.execute(delete)
    db.commit()


def update_student(db, data , id ):
    query = update(models.Student).where(models.Student.user_student_number==id).values(**data.dict(exclude={'course_professor_IDL'}))
    db.execute(query)
    db.commit()

def select_student(db, id) :
    results = (
        db.query(models.Student, models.association_table.c.course_id, models.association_table.c.user_professor_id)
        .outerjoin(models.association_table, models.Student.user_student_number == models.association_table.c.user_student_number)
        .filter(models.Student.user_student_number == id)
        .all()
    )

    student_data = {}
    course_professor_IDL = {}

    for result in results:
        student, course_id, professor_id = result
        if not student_data:
            student_data = {
                "user_Fname": student.user_Fname,
                "user_Lname": student.user_Lname,
                "user_birthday": student.user_birthday,
                "user_ID": student.user_ID,
                "user_province": student.user_province,
                "user_borncity": student.user_borncity,
                "user_address": student.user_address,
                "user_postal_code": student.user_postal_code,
                "user_phone_number": student.user_phone_number,
                "user_home_number": student.user_home_number,
                "user_department": student.user_department,
                "user_major": student.user_major,
                "user_student_number": student.user_student_number,
                "user_student_father_name": student.user_student_father_name,
                "user_student_IDS": student.user_student_IDS,
                "user_student_married": student.user_student_married
            }

        if course_id and professor_id:
            if professor_id not in course_professor_IDL:
                course_professor_IDL[professor_id] = set()
            course_professor_IDL[professor_id].add(course_id)

    student_data["course_professor_IDL"] = str({k: v for k, v in course_professor_IDL.items()})

    return student_data