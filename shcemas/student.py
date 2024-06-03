from typing import ClassVar
from shcemas.user import user_Info
from fastapi import HTTPException
from pydantic import root_validator 
from re import match , fullmatch
from database.CRUD.course import read_course , session
from database.CRUD.professor import Create_professor
import ast
class Student_Info(user_Info):

    user_student_number : str
    user_student_father_name : str
    user_student_IDS : str 
    user_student_married : str 
    # user_student_courses_IDs : str 
    # user_student_professors_IDs : str 
    course_professor_IDL : str 
    p_c : ClassVar[dict]={}
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
            # pattern = r'^\d{6}-\d{2}-[ا-ی]$'
            # if match(pattern,ids)== None : detail['user_IDS']='سریال شناسنامه نامعتبر است'
            pass

        def student_married_check(married,detail):
            if married != 'متاهل' and married != 'مجرد' : detail['student_married']='وضیعت تاهل وارد شده نامعتبر است'
            return detail
        
        # def student_student_courses_IDs(course_id,detail,db):
        #     Ids=course_id.split('-')
        #     for i in Ids :
        #         if read_course(db=db,id=i)==None:
        #             detail[f'student_student_courses_IDs: {i}']=(f'کد درس :{i} نامعتبر است')
        #     return detail
        
        def check_course_professor(p_c,detail,db):
            p_c=eval(p_c)
            list_professor = p_c.keys()
            for i in list_professor :
                if i.isdigit()==False or Create_professor.read_professor(db=db , p_id=i)==None:
                    detail[f'course_professor_IDL{i}']=f'کد استاد {i} وارد شده نامعتبر است'
                    continue
                for j in p_c[i] :
                    if Create_professor.read_relationship_CR(db=db , id_p=i, id_c=j)==None:
                        detail[f'course_professor_IDL{i}']=f'برای استاد با کد {i} کد درس {j}موجود نیست '
            return detail
        student_number_check(values['user_student_number'], cls.detail)
        student_father_name(values['user_student_father_name'],cls.detail)
        student_IDS_check(values['user_student_IDS'],cls.detail)
        student_married_check(values['user_student_married'],cls.detail)
        # student_student_courses_IDs(values['student_student_courses_IDs'], cls.detail ,session)
        check_course_professor(values['course_professor_IDL'],cls.detail,session)

        if cls.detail != {} :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        
        cls.p_c= values['course_professor_IDL']

        values.pop('course_professor_IDL')
        
        return values  
    