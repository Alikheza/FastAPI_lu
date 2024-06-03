from fastapi import HTTPException
from pydantic import BaseModel , root_validator 
from typing import ClassVar
from re import fullmatch

class Course_Info_In(BaseModel):

    course_id : str
    course_name : str
    course_department : str
    course_credit : str
    detail : ClassVar = {}

    @root_validator(skip_on_failure=True)
    def course_info_check (cls,values):


        def course_ID_check(Id,detail):
            if Id.isdigit()==False or len(Id)!=5 :
                detail['course_ID']= 'کد درس وارد شده معتبر نمیباشد ، کد درس یک عدد 5 رقمی میتواند باشد'
            return detail

        def course_name_check(name, detail):
            pattern = r"^[ا-ی]+$"
            if len(name)>25 : detail['course_name'] = 'نام نمیتواند بیشتر از 25 کاراکتر باشد'
            elif fullmatch(pattern,name)== None: detail['course_name'] = 'نام فقط میتواند حاوی کارکتر های فارسی باشد'
            return detail

        def course_department_check(department,detail):
            department_list =['فنی و مهندسی','علوم پایه','علوم انسانی','دامپزشکی','اقتصاد','کشاورزی','منابع طبیعی']
            if department not in department_list : detail['course_department']='دانشکده وارد شده معتبر نمی باشد'
            return detail
        
        def course_credit_check(credit,detail):
            if credit not in str(range(2,4)):detail['course_credit']='مقدار وارد شده معتبر نمیباشد، مقدار معتبر عددی بین ۱ تا ۴ است'
            return detail
        
        course_ID_check(values['course_id'],cls.detail)
        course_name_check(values['course_name'],cls.detail)
        course_department_check(values['course_department'],cls.detail)
        course_credit_check(values['course_credit'],cls.detail)

        if cls.detail != {} :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        return values  

class Course_Info_Out(BaseModel):
    course_name : str
    course_department : str
    course_credit : int