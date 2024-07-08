from fastapi import APIRouter , Depends , HTTPException , Body
from typing import Annotated
from sqlalchemy.orm import Session
from shcemas import student as STU 
from database.CRUD import student as S_crud 
from app.dependency import get_db
from app import authentication
from fastapi.security import  OAuth2PasswordRequestForm



router = APIRouter()


@router.post('/v1/Student_login', status_code=200)
def login_student_API(data: OAuth2PasswordRequestForm = Depends(), db : Session=Depends(get_db)):
    result = S_crud.read_student_ID_(db=db, id=data.password)
    if result==None or data.username!='student': raise HTTPException(detail='رمز عبور یا نام کاربری اشتباه میباشد', status_code=403)
    token = authentication.create_access_token(data=data)
    return {"access_token": token, "token_type": "bearer"}


@router.post('/v1/Register_Student',  status_code=201)
def create_student_API(Student_validate:STU.Student_Info,current_user: Annotated[str, Depends(authentication.get_current_admin)], db : Session=Depends(get_db)):
    if S_crud.read_student_ID(db=db, s_id= Student_validate.user_student_number ) != None : raise HTTPException(status_code=400,detail=f'شماره دانشجوی نمیتواند تکراری باشد')
    S_crud.create_student_db(data=Student_validate , db=db)
    return 'ثبت اطلاعات دانشجو موفقیت امیز بود'


@router.get('/v1/Read_Student/{student_num}' , response_model= STU.Student_Info_Out , status_code=200)
def read_student_API(student_num, current_user: Annotated[str, Depends(authentication.get_current_student)], db : Session=Depends(get_db)):
    id = S_crud.read_student_ID_(db=db, id= current_user['id']).user_student_number
    if current_user['Role']!='student' or student_num!=id : raise HTTPException(status_code=403, detail='شما مجوز دسترسی به این بخش را ندارید')
    result = S_crud.read_student_ID(db=db, s_id= student_num)
    if result==None : raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    return result


@router.put('/v1/Update_Student/{student_num}' , status_code=201)
def update_student_API(student_num:str,current_user: Annotated[str, Depends(authentication.get_current_student)], update_student:dict=Body(),db : Session=Depends(get_db)):
    id = S_crud.read_student_ID_(db=db, id= current_user['id']).user_student_number
    if current_user['Role']!='student' or student_num!=id : raise HTTPException(status_code=403, detail='شما مجوز دسترسی به این بخش را ندارید')
    result = S_crud.read_student_ID(db=db, s_id= student_num)
    if result==None : raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    else : 
        select_student=S_crud.select_student(db=db, id= student_num)
        temp={**select_student, **update_student}
        data = STU.Student_Info(**temp)
        S_crud.update_student(data=data , db=db,id=student_num,lid=select_student["course_professor_IDL"])
    return 'اپدیت اطلاعات دانشجو موفقیت امیز بود'


@router.delete('/v1/Delete_Student/{student_num}' , status_code=200)
def delete_student_API(student_num,current_user: Annotated[str, Depends(authentication.get_current_student)], db : Session=Depends(get_db)):
    id = S_crud.read_student_ID_(db=db, id= current_user['id']).user_student_number
    if current_user['Role']!='student' or student_num!=id : raise HTTPException(status_code=403, detail='شما مجوز دسترسی به این بخش را ندارید')
    if S_crud.read_student_ID(db=db, s_id= student_num)==None : raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    else : S_crud.delete_student(db=db, s_id=student_num)
    return f'اطلاعات دانشجو با شماره دانشجوی {student_num}حذف شد'


@router.delete('/v1/Delete_Student_Course/{student_num}/{course_id}' , status_code=200)
def delete_student_course_API(student_num,current_user: Annotated[str, Depends(authentication.get_current_student)], course_id, db : Session=Depends(get_db)):
    id = S_crud.read_student_ID_(db=db, id= current_user['id']).user_student_number
    if current_user['Role']!='student' or student_num!=id : raise HTTPException(status_code=403, detail='شما مجوز دسترسی به این بخش را ندارید')
    if S_crud.read_student_ID(db=db, s_id= student_num)==None : raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    else : S_crud.delete_student_course(db=db, s_id=student_num,c_id=course_id)
    return f'درس دانشجو با شماره دانشجوی {student_num}حذف شد'