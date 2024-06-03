from typing import ClassVar
from shcemas.user import user_Info
from fastapi import HTTPException 
from pydantic import root_validator 
from database.CRUD import course , professor


class Professor_Info_In(user_Info):

    user_professor_id : str 
    user_professor_course_IDs : str
    C_Id : ClassVar =''

    @root_validator(skip_on_failure=True)
    def professor_info_check(cls,values):
        cls.C_Id= ''
        user_Info.user_info_check(cls,values)
        
        def professor_id_check(Id,detail,db):
            print('here1')
            if Id.isdigit()==False or len(Id)!=6 : detail['user_professor_id']= 'کد استاد وارد شده معتبر نمیباشد ، کد استاد یک عدد ۶ رقمی میتواند باشد'
            
            elif professor.read_professor(db=db, p_id=Id)!= None : detail['user_professor_id']= 'کد استاد وارد شده نمیتواند تکراری باشد'
            print('here')
            return detail
        
        def professor_course_ID_check(course_id,detail, db):
            Ids=course_id.split('-')
            for i in Ids :
                if course.read_course(db=db,id=i)==None or i.isdigit()==False:
                    detail[f'user_professor_course_ID : {i}']=(f'کد درس :{i} نامعتبر است')
            return detail
        professor_id_check(values['user_professor_id'],cls.detail,course.session)
        professor_course_ID_check(values['user_professor_course_IDs'], cls.detail ,course.session) 

        if cls.detail != {} :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        
        cls.C_Id = values['user_professor_course_IDs']

        values.pop('user_professor_course_IDs')

        return  values
