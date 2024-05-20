from shcemas import user
from fastapi import HTTPException
from pydantic import root_validator 

class Professor_Info(user.user_check):

    Lid : str 
    LcourseIDs : str
    
    @root_validator(skip_on_failure=True)
    def professor_info_check(cls,values,detail):

        def professor_id_check(Id,detail):
            if Id.isdigit()==False or len(Id)!=6 : detail['Lid']= 'کد استاد وارد شده معتبر نمیباشد ، کد استاد یک عدد ۶ رقمی میتواند باشد'
            return detail
        
        def professor_course_ID_check():
            pass
        
        professor_id_check(values['Lid'],detail)
        professor_course_ID_check()

        if detail != {} :
            raise HTTPException(detail=detail,status_code=400)
        return values  