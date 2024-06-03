from database import module 

class Create_Student :
    
    def student (db, data):
        db_S = module.Student(**data.dict())
        db.add(db_S)
        db.commit()
        db.refresh(db_S)
        p_c= data.p_c
        p_c=eval(p_c)
        s_id = data.user_student_number
        p_id = p_c.keys()
        for i in p_id :
            for j in p_c[i] :
                Create_Student.student_R(db,p_id=i,c_id=j , s_id = s_id)  
   
    def student_R (db, p_id , c_id , s_id):
        db_SR = module.Relation_table(user_student_number= s_id, course_id=c_id ,user_professor_id=p_id)
        db.add(db_SR)
        db.commit()
        db.refresh(db_SR)
        return 'ثبت اطلعات دانشجو موفقیت امیز بود'
    
