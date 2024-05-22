from shcemas.user import user_Info
from fastapi import HTTPException
from pydantic import root_validator 
from re import match , fullmatch
class Student_Info(user_Info):

    user_student_number : str
    user_student_father_name : str
    user_student_IDS : str 
    user_student_married : str 
    user_student_courses_ID : str 
    
    @root_validator(skip_on_failure=True)
    def student_info_check(cls,values):
        user_Info.user_info_check(cls,values)

        def student_number_check(studentnumber,detail):
            if len(studentnumber) != 11 or studentnumber.isdigit() == False : detail['user_student_number']='شماره دانشجوی  باید ۱۱ رقم باشد. تعداد ارقام وارد شده درست نمیباشد. '
            elif int(studentnumber[0:3]) not in range (400,403): detail['user_student_number']='قسمت سال نادرست است '
            elif studentnumber[3:9] != '114150' : detail['user_student_number']='قسمت ثابت نادرست است'
            elif int(studentnumber[9:]) not in range(1,100): detail['user_student_number']='قسمت اندیس نادرست است'
            return detail
        
        def student_father_name (Fname,detail):
            pattern = r"^[آ-ی]+$"
            if len(Fname)>10 : detail['user_father_name'] = 'نام پدر نمیتواند بیشتر از ۱۰ کاراکتر باشد'
            elif fullmatch(pattern,Fname)== None: detail['user_father_name'] = 'نام پدر فقط میتواند حاوی کارکتر های فارسی باشد'
            return detail
        
        def student_IDS_check(ids , detail):
            pattern = r'^\d{6}-\d{2}-[ا-ی]$'
            if match(pattern,ids)== None : detail['user_IDS']='سریال شناسنامه نامعتبر است'

        def student_married_check(married,detail):
            if married != 'متاهل' and married != 'مجرد' : detail['student_married']='وضیعت تاهل وارد شده نامعتبر است'
            return detail
        
        def student_student_courses_ID():
            pass
        
        student_number_check(values['user_student_number'], cls.detail)
        student_father_name(values['user_student_father_name'],cls.detail)
        student_IDS_check(values['user_student_IDS'],cls.detail)
        student_married_check(values['user_student_married'],cls.detail)

        student_student_courses_ID()

        if cls.detail != {} :
            raise HTTPException(detail=cls.detail,status_code=400)
        return values  