from typing import ClassVar
from shcemas.user import user_Info
from fastapi import HTTPException 
from pydantic import root_validator , BaseModel
from database.CRUD import course 


class Professor_Info_In(user_Info):


    user_professor_id : str 
    # user_professor_course_IDs : str
    C_Id : ClassVar =''

    @root_validator(pre=True)
    def professor_info_check(cls,values):
        cls.C_Id= ''
        user_Info.user_info_check(cls,values)
        
        def professor_id_check(Id,detail):
            if Id.isdigit()==False or len(Id)!=6 : detail['user_professor_id']= 'کد استاد وارد شده معتبر نمیباشد ، کد استاد یک عدد ۶ رقمی میتواند باشد'
            return detail
        
        def professor_course_ID_check(course_id,detail, db):
            Ids=course_id.split('-')
            for i in Ids :
                if course.read_course(db=db,id=i)==None or i.isdigit()==False:
                    detail[f'user_professor_course_ID : {i}']=(f'کد درس :{i} نامعتبر است')
            return detail
        try:
            professor_id_check(values['user_professor_id'],cls.detail)
            professor_course_ID_check(values['user_professor_course_IDs'], cls.detail ,course.session) 

        except  KeyError as ke: 
            raise HTTPException(detail=f'  وارد نشده است {ke!r}',status_code=400)

        if cls.detail != {} :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        
        cls.C_Id = values['user_professor_course_IDs']
        
        values.pop('user_professor_course_IDs')

        return  values

class Professor_Info_Out(BaseModel):
    user_Fname : str 
    user_Lname : str
    user_professor_id : int
    user_ID : int