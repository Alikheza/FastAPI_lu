from typing import ClassVar
from shcemas.user import user_Info
from fastapi import HTTPException
from pydantic import root_validator , BaseModel
from re import match , fullmatch
from database.CRUD import professor , student
from database.connect import session

class Student_Info(user_Info):
     
    '''  
    After the 'user' class validates general parameters provided by the user and records any issues in the 'detail' dictionary, 
    the 'student' class now validates parameters specific to student. 
    Finally, after updating the 'detail' dictionary with any additional issues, the validation errors are displayed to the user.

    
    To ensure the parameters are correctly validated, they must be sent according to the names listed below.
    '''
    
    user_student_number : str
    user_student_father_name : str
    user_student_IDS : str 
    user_student_married : str 
    #course_professor_IDL : str
    p_c : ClassVar[dict]={}

    @root_validator(pre=True)
    def student_info_check(cls,values):
        user_Info.user_info_check(cls,values)

        def student_number_check(studentnumber,detail):
            if len(studentnumber) != 11 or studentnumber.isdigit() == False : detail['user_student_number']='شماره دانشجوی  باید ۱۱ رقم باشد. تعداد ارقام وارد شده درست نمیباشد. '
            elif int(studentnumber[0:3]) not in range (400,403): detail['user_student_number']='قسمت سال نادرست است '
            elif studentnumber[3:9] != '114150' : detail['user_student_number']='قسمت ثابت نادرست است'
            elif int(studentnumber[9:]) not in range(1,100): detail['user_student_number']='قسمت اندیس نادرست است'
        
        def student_father_name (Fname,detail):
            pattern = r"^[آ-ی]+$"
            if len(Fname)>10 : detail['user_father_name'] = 'نام پدر نمیتواند بیشتر از ۱۰ کاراکتر باشد'
            elif fullmatch(pattern,Fname)== None: detail['user_father_name'] = 'نام پدر فقط میتواند حاوی کارکتر های فارسی باشد'
        
        def student_IDS_check(ids , detail , db):
            pattern = r'^\d{6}-\d{2}-[ا-ی]$'
            if student.select_user_IDs(db=db , ids=ids)!=None: detail['user_student_IDS']='سریال شناسنامه تکراری است'
            elif match(pattern,ids)== None : detail['user_student_IDS']='سریال شناسنامه نامعتبر است'

        def student_married_check(married,detail):
            if married != 'متاهل' and married != 'مجرد' : detail['student_married']='وضیعت تاهل وارد شده نامعتبر است'

        def check_course_professor(p_c,detail,db):
            p_c=eval(p_c)
            list_professor = p_c.keys()
            for i in list_professor :
                if i.isdigit()==False or professor.read_professor(db=db , p_id=i)==None:
                    detail[f'course_professor_IDL{i}']=f'کد استاد {i} وارد شده نامعتبر است'
                    continue
                for j in p_c[i] :
                    if type(j)!=str : j = str(j)
                    if professor.read_relationship_CR(db=db , id_p=i, id_c=j)==None:
                        detail[f'course_professor_IDL{i}']=f'برای استاد با کد {i} کد درس {j}موجود نیست '

        def student_ID_check(id,detail,db):
            if student.select_user_ID(db=db , id=id )!= None : detail['user_ID']='کد ملی تکراری است'

        '''calling the checking-functions use try to see any of parameters are send or not'''

        try:
            student_ID_check(values['user_ID'],cls.detail,session)
            student_number_check(values['user_student_number'], cls.detail)
            student_father_name(values['user_student_father_name'],cls.detail)
            student_IDS_check(values['user_student_IDS'],cls.detail , session)
            student_married_check(values['user_student_married'],cls.detail)
            check_course_professor(values['course_professor_IDL'],cls.detail,session)

        except  KeyError as ke: 
            raise HTTPException(detail=f'  وارد نشده است {ke!r}',status_code=400)
        
        if cls.detail != {} :
            error = cls.detail
            cls.detail = {}
            raise HTTPException(detail=error,status_code=400)
        
        cls.p_c= values['course_professor_IDL']

        values.pop('course_professor_IDL')
        
        return values  
    
class Student_Info_Out(BaseModel):
    user_Fname : str 
    user_Lname : str
    user_student_father_name : str
    user_student_number : str
    class Config :
        from_attributes = True