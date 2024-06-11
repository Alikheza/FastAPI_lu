from fastapi import APIRouter , Depends , HTTPException , Body
from sqlalchemy.orm import Session
from shcemas import course as COR  
from database.CRUD import course as C_crud
from dependency import get_db


router = APIRouter()


@router.post('/Register_Course', status_code=201)
def create_course_API(course_validate:COR.Course_Info_In, db : Session=Depends(get_db)):
    if C_crud.read_course(db=db,id=course_validate.course_id) != None : raise HTTPException(status_code=400,detail='کد درس نمیتواند تکراری باشد')
    return C_crud.create_course(data=course_validate , db=db)


@router.get("/Read_course/{course_id}", response_model=COR.Course_Info_Out , status_code=200)
def read_course_API(course_id:str , db:Session = Depends(get_db)):
    result = C_crud.read_course(db=db,id=course_id)
    if result==None : 
        raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    return result

@router.put("/Update_course/{course_id}", status_code=201)
def update_course_API(course_id:str , update_course:dict = Body() , db:Session = Depends(get_db)):
    result = C_crud.read_course(db=db,id=course_id)
    if result==None : 
        raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    else:
        temp={**result.__dict__,**update_course }
        data=COR.Course_Info_In(**temp)
        C_crud.update_course(db=db,id=course_id,data=data)
        return f'اطلعات درس با کد درسی {course_id} اپدیت شد '

@router.delete("/Delete_course/{course_id}", status_code=200)
def delete_course_API(course_id:str , db:Session = Depends(get_db)):
    if C_crud.read_course(db=db,id=course_id)==None :
        raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    else:
        C_crud.delete_course(db=db,id=course_id)
        return f' اطلعات درس با کد درسی  {course_id} حذف شد ' 
    