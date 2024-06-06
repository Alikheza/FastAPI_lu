from database import module 
from sqlalchemy import delete , update 
    
def create_student_db (db, data):
    db_S = module.Student(**data.dict())
    db.add(db_S)
    db.commit()
    db.refresh(db_S)
    p_c= eval(data.p_c)
    s_id = data.user_student_number
    p_id = p_c.keys()
    for i in p_id :
        for j in p_c[i] :
            student_R(db,p_id=i,c_id=j , s_id = s_id)  
    return 'ثبت اطلعات دانشجو موفقیت امیز بود'
    
   
def student_R (db, p_id , c_id , s_id):
    db_SR = module.Relation_table(user_student_number= s_id, course_id=c_id ,user_professor_id=p_id)
    query = delete(module.Relation_table).where(module.Relation_table.course_id==c_id).where(module.Relation_table.user_professor_id==p_id).where(module.Relation_table.user_student_number==None)
    db.add(db_SR)
    db.execute(query)
    db.commit()
    db.refresh(db_SR)
    
def read_student_ID (db,s_id:str):
    return db.query(module.Student).filter(module.Student.user_student_number==s_id).first()

def delete_student (db , s_id ):
    query =  delete(module.Student).where(module.Student.user_student_number==s_id)
    query2 = update(module.Relation_table).where(module.Relation_table.user_student_number==s_id).values(user_student_number=None)
    db.execute(query2)
    db.execute(query)
    db.commit()

def select_student (db , id ):
    left_outer_join = (
        db.query(module.Student, module.Relation_table)
        .outerjoin(module.Relation_table, module.Student.user_student_number == module.Relation_table.user_student_number)
        .filter(module.Student.user_student_number == id)
    )

    right_outer_join = (
        db.query(module.Student, module.Relation_table)
        .outerjoin(module.Student, module.Student.user_student_number == module.Relation_table.user_student_number)
        .filter(module.Relation_table.user_student_number == id)
    )

    full_outer_join = left_outer_join.union_all(right_outer_join)
    
    results = full_outer_join.all()
    student_data = {}
    course_professor_IDL = {}

    for student, relation in results:
        if student and not student_data:
            student_data.update({
                "user_Fname": student.user_Fname,
                "user_Lname": student.user_Lname,
                "user_birthday": student.user_birthday,
                "user_ID": str(student.user_ID),
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
            })

        if relation:
            professor_id = relation.user_professor_id
            course_id = relation.course_id
            if professor_id not in course_professor_IDL:
                course_professor_IDL[professor_id] = set()
            course_professor_IDL[professor_id].add(course_id)

    student_data["course_professor_IDL"] =str( {k: v for k, v in course_professor_IDL.items()})

    return student_data


def update_student(db, data , id):
    query = delete(module.Relation_table).where(module.Relation_table.user_student_number==id)
    db.execute(query)
    query = update(module.Student).where(module.Student.user_student_number==id).values(user_student_number=data.user_student_number)
    db.execute(query)
    db.commit()
    p_c= eval(data.p_c)
    s_id = data.user_student_number
    p_id = p_c.keys()
    for i in p_id :
        for j in p_c[i] :
            student_R(db,p_id=i,c_id=j , s_id = s_id)   
    query = update(module.Student).where(module.Student.user_student_number==data.user_student_number).values(**data.dict())
    db.execute(query)
    db.commit()
    return 'اپدیت اطلعات دانشجو موفقیت امیز بود'
