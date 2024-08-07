from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException , Body
from sqlalchemy.orm import Session
from shcemas import course as COR  
from database.CRUD import course as C_crud
from app.dependency import get_db
from app import authentication

router = APIRouter()


@router.post('/v1/Register_Course', status_code=201)
def create_course_API(course_validate:COR.Course_Info_In, current_user: Annotated[str, Depends(authentication.get_current_admin)],db : Session=Depends(get_db)):
    if C_crud.read_course(db=db,id=course_validate.course_id) != None : raise HTTPException(status_code=400,detail='کد درس نمیتواند تکراری باشد')
    C_crud.create_course(data=course_validate , db=db)
    return 'ثبت اطلاعات درس موفقیت امیز بود'

@router.get("/v1/Read_course/{course_id}", response_model=COR.Course_Info_Out , status_code=200)
def read_course_API(course_id:str, current_user: Annotated[str, Depends(authentication.get_current_admin)], db:Session = Depends(get_db)):
    result = C_crud.read_course(db=db,id=course_id)
    if result==None : raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    return result

@router.put("/v1/Update_course/{course_id}", status_code=201)
def update_course_API(course_id:str,current_user: Annotated[str, Depends(authentication.get_current_admin)], update_course:dict = Body() , db:Session = Depends(get_db)):
    result = C_crud.read_course(db=db,id=course_id)
    if result==None : raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    else:
        temp={**result.__dict__,**update_course }
        data=COR.Course_Info_In(**temp)
        C_crud.update_course(db=db,id=course_id,data=data)
    return f'اطلاعات درس با کد درسی {course_id} اپدیت شد '

@router.delete("/v1/Delete_course/{course_id}", status_code=200)
def delete_course_API(course_id:str,current_user: Annotated[str, Depends(authentication.get_current_admin)],db:Session = Depends(get_db)):
    if C_crud.read_course(db=db,id=course_id)==None : raise HTTPException(status_code=404,detail=f'درس با کد درسی {course_id} پیدا نشد')
    else : C_crud.delete_course(db=db,id=course_id)
    return f' اطلاعات درس با کد درسی  {course_id} حذف شد ' 
    