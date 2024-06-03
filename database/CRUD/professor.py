from sqlalchemy.orm import Session 
from database import module 
from shcemas.professor import Professor_Info_In

    
def professor_R(db, p_id , c_id):
    db_PR=module.Relation_table(course_id = c_id , user_professor_id = p_id)
    db.add(db_PR)
    db.commit()
    db.refresh(db_PR)
def professor(db,data):
    db_pro=module.Professor(**data.dict())
    db.add(db_pro)
    db.commit()
    db.refresh(db_pro)
    id = Professor_Info_In.C_Id .split('-')
    for i in  id:
        professor_R(db=db , p_id=data.user_professor_id, c_id = i )
    return 'ثبت اطلعات استاد موفقیت امیز بود'

def read_professor(db,p_id):
    return db.query(module.Professor).filter(module.Professor.user_professor_id==p_id).first()

def read_relationship_CR(db, id_p:int , id_c:int):
    return db.query(module.Relation_table).filter(module.Relation_table.course_id==id_c , module.Relation_table.user_professor_id==id_p).first()