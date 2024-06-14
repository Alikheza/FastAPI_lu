from sqlalchemy import delete , update
from database import models 

def create_professor(db,data):
    db_pro=models.Professor(**data.dict())
    db.add(db_pro)
    db.commit()
    db.refresh(db_pro)
    professor_R(db=db ,data=data )
    
def professor_R(db, data):
    for i in data.C_Id.split('-'):
        db_PR=models.Relation_table(course_id = i , user_professor_id = data.user_professor_id)
        db.add(db_PR)
    db.commit()
    db.refresh(db_PR)
    

def read_professor(db,p_id):
    return db.query(models.Professor).filter(models.Professor.user_professor_id==p_id).first()

def read_relationship_CR(db, id_p , id_c):
    return db.query(models.Relation_table).filter(models.Relation_table.course_id==id_c , models.Relation_table.user_professor_id==id_p).first()




def delete_professor(db,id):
    query =  delete(models.Professor).where(models.Professor.user_professor_id==id)
    db.execute(query)
    db.commit()


def update_professor(db, data , id ):
    query = update(models.Professor).where(models.Professor.user_professor_id==id).values(user_professor_id=data.user_professor_id)
    db.execute(query)
    db.commit()





def select_professor(db , id):
    left_outer_join = (
        db.query(models.Professor, models.Relation_table)
        .outerjoin(models.Relation_table, models.Professor.user_professor_id == models.Relation_table.user_professor_id)
        .filter(models.Professor.user_professor_id == id)
    )

    right_outer_join = (
        db.query(models.Professor, models.Relation_table)
        .outerjoin(models.Relation_table, models.Professor.user_professor_id == models.Relation_table.user_professor_id)
        .filter(models.Professor.user_professor_id == id)
    )
    full_outer_join = left_outer_join.union_all(right_outer_join)
    
    results = full_outer_join.all()
    
    professor_data = {}
    user_professor_course_IDs = []

    for professor, relation in results:
        if professor_data == {}:
            professor_data.update({
                "user_Fname": professor.user_Fname,
                "user_Lname": professor.user_Lname,
                "user_birthday": professor.user_birthday,
                "user_ID": str(professor.user_ID),
                "user_province": professor.user_province,
                "user_borncity": professor.user_borncity,
                "user_address": professor.user_address,
                "user_postal_code": str(professor.user_postal_code),
                "user_phone_number": str(professor.user_phone_number),
                "user_home_number": str(professor.user_home_number),
                "user_department": professor.user_department,
                "user_major": professor.user_major,
                "user_professor_id": professor.user_professor_id
            })

        if relation:
            course_id = relation.course_id
            if course_id not in user_professor_course_IDs:
                user_professor_course_IDs.append(course_id)
    formatstr = '-'.join(user_professor_course_IDs)
    professor_data['user_professor_course_IDs']=formatstr 
 
    return professor_data

def select_user_ID(db,id):
    return db.query(models.Professor).filter(models.Professor.user_ID==id).first()