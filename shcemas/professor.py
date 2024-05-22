from shcemas.user import user_Info
from fastapi import HTTPException
from pydantic import root_validator 

class Professor_Info(user_Info):

    user_professor_id : str 
    user_professor_course_IDs : str
    
    @root_validator(skip_on_failure=True)
    def professor_info_check(cls,values):
                
        user_Info.user_info_check(cls,values)
        
        def professor_id_check(Id,detail):
            if Id.isdigit()==False or len(Id)!=6 : detail['user_professor_id']= 'کد استاد وارد شده معتبر نمیباشد ، کد استاد یک عدد ۶ رقمی میتواند باشد'
            return detail
        
        def professor_course_ID_check():
            pass

        professor_id_check(values['user_professor_id'],cls.detail)
        professor_course_ID_check()

        if cls.detail != {} :
            raise HTTPException(detail=cls.detail,status_code=400)
        return values  