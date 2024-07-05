from typing import ClassVar
from shcemas.user import user_Info
from fastapi import HTTPException 
from pydantic import BaseModel ,model_validator
from database.CRUD import course 
from database.connect import session


class Professor_Info_In(user_Info):

    '''
    After the 'user' class validates general parameters provided by the user and records any issues in the 'detail' dictionary, 
    the 'professor' class now validates parameters specific to professor. 
    Finally, after updating the 'detail' dictionary with any additional issues, the validation errors are displayed to the user.
    

    To ensure the parameters are correctly validated, they must be sent according to the names listed below.
    '''

    user_professor_id : str 
    user_professor_course_IDs : str

    @model_validator(mode='before')
    def professor_info_check(cls,values):
        user_Info.user_info_check(cls,values)
        
        def professor_id_check(Id,detail):
            if Id.isdigit()==False or len(Id)!=6 : detail['user_professor_id']= 'کد استاد وارد شده معتبر نمیباشد ، کد استاد یک عدد ۶ رقمی میتواند باشد'
            

        def professor_course_ID_check(course_id,detail, db):
            Ids=course_id.split('-')
            for i in Ids :
                if course.read_course(db=db,id=i)==None or i.isdigit()==False : detail[f'user_professor_course_IDs  {i}']=(f'کد درس {i} نامعتبر است')

        try:
            professor_id_check(values['user_professor_id'],cls.detail)
            professor_course_ID_check(values['user_professor_course_IDs'], cls.detail ,session) 

        except  KeyError as ke: 
            raise HTTPException(detail=f'  وارد نشده است {ke!r}',status_code=400)

        if cls.detail :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        

        return  values

class Professor_Info_Out(BaseModel):
    user_Fname : str 
    user_Lname : str
    user_professor_id : str
    user_ID : str