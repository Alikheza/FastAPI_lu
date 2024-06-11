from fastapi import APIRouter , Depends , HTTPException , Body
from sqlalchemy.orm import Session
from shcemas import student as STU 
from database.CRUD import student as S_crud 
from dependency import get_db



router = APIRouter()


@router.post('/Register_Student',  status_code=201)
def create_student_API(Student_validate:STU.Student_Info, db : Session=Depends(get_db)):
    if S_crud.read_student_ID(db=db, s_id= Student_validate.user_student_number ) != None : raise HTTPException(status_code=400,detail=f'شماره دانشجوی نمیتواند تکراری باشد')
    S_crud.create_student_db(data=Student_validate , db=db)
    return 'ثبت اطلعات دانشجو موفقیت امیز بود'


@router.get('/Read_Student/{student_num}' , response_model= STU.Student_Info_Out , status_code=200)
def read_student_API(student_num, db : Session=Depends(get_db)):
    result = S_crud.read_student_ID(db=db, s_id= student_num)
    if result==None : 
        raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    return result

@router.put('/Update_Student/{student_num}' , status_code=201)
def update_student_API(student_num:str, update_student:dict=Body(),db : Session=Depends(get_db)):
    result = S_crud.read_student_ID(db=db, s_id= student_num)
    if result==None : 
        raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    else : 
        temp={**S_crud.select_student(db=db, id= student_num), **update_student}
        data = STU.Student_Info(**temp)
        S_crud.update_student(data=data , db=db,id=student_num)
        return 'اپدیت اطلعات دانشجو موفقیت امیز بود'

@router.delete('/Delete_Student/{student_num}' , status_code=200)
def delete_student_API(student_num, db : Session=Depends(get_db)):
    if S_crud.read_student_ID(db=db, s_id= student_num)==None: 
        raise HTTPException(status_code=404,detail=f'دانشجو با شماره دانشجوی {student_num} پیدا نشد')
    else :
        S_crud.delete_student(db=db, s_id=student_num)
    return f'اطلعات دانشجو با شماره دانشجوی {student_num}حذف شد'

