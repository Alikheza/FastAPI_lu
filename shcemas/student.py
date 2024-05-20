from shcemas import user
from fastapi import HTTPException
from pydantic import root_validator 
import re
class Student_Info(user.user_check):

    user_student_number : str
    user_father_name : str
    user_married : str 
    user_student_courses_ID : str 
    

    @root_validator(skip_on_failure=True)
    def student_info_check(cls,values,detail):

        def student_number_check(studentnumber,detail):
            if len(studentnumber) != 11 or studentnumber.isdigit() == False : detail['user_student_number']='شماره دانشجوی  باید ۱۱ رقم باشد. تعداد ارقام وارد شده درست نمیباشد. '
            elif int(studentnumber[0:3]) not in range (400,403): detail['user_student_number']='قسمت سال نادرست است '
            elif studentnumber[3:9] != '114150' : detail['user_student_number']='قسمت ثابت نادرست است'
            elif int(studentnumber[9:]) not in range(1,100): detail['user_student_number']='قسمت اندیس نادرست است'
            return detail
        
        def student_father_name (Fname,detail):
            pattern = r"^[آ-ی]+$"
            if len(Fname)>10 : detail['user_father_name'] = 'نام پدر نمیتواند بیشتر از ۱۰ کاراکتر باشد'
            elif re.fullmatch(pattern,Fname)== None: detail['user_father_name'] = 'نام پدر فقط میتواند حاوی کارکتر های فارسی باشد'
            return detail

        def student_married_check(married,detail):
            if married != 'متاهل' and married != 'مجرد' : detail['student_married']='وضیعت تاهل وارد شده نامعتبر است'
            return detail
        
        def student_student_courses_ID():
            pass
        
        student_number_check(values['user_student_number'], detail)
        student_father_name(values['user_father_name'],detail)
        student_married_check(values['user_married'],detail)
        student_student_courses_ID()

        if detail != {} :
            raise HTTPException(detail=detail,status_code=400)
        return values  