from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException , Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from shcemas import professor as POR
from database.CRUD import professor as P_crud
from app.dependency import get_db
from app import authentication

 
router = APIRouter()


@router.post("/v1/professor_login")
def login_professor_API(data: OAuth2PasswordRequestForm = Depends() , db:Session=Depends(get_db)):
    result = P_crud.read_professor_ID(db=db, id=data.password)
    if result==None or data.username!='professor': raise HTTPException(detail='رمز عبور یا نام کاربری اشتباه میباشد', status_code=403)
    token = authentication.create_access_token(data=data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/v1/Register_professor" , status_code=201)
def create_professor_API(professor_validation: POR.Professor_Info_In ,current_user: Annotated[str, Depends(authentication.get_current_admin)], db:Session=Depends(get_db)):
    if P_crud.read_professor(db=db, p_id=professor_validation.user_professor_id)!= None : raise HTTPException(detail='کد استاد وارد شده نمیتواند تکراری باشد', status_code=400)
    P_crud.create_professor(db=db , data= professor_validation)
    return 'ثبت اطلاعات استاد موفقیت امیز بود'

@router.get("/v1/Read_professor/{professor_id}" ,response_model=POR.Professor_Info_Out , status_code=200)
def read_professor_API(professor_id:str ,current_user: Annotated[str, Depends(authentication.get_current_professor)],db:Session=Depends(get_db)):
    id=P_crud.read_professor_ID(db=db, id=current_user['id']).user_professor_id
    if current_user['Role']!='professor' or professor_id!=id : raise HTTPException(detail='شما مجوز دسترسی به این بخش را ندارید', status_code=403)
    result = P_crud.read_professor(db=db, p_id=professor_id)
    if result==None : raise HTTPException(detail=f'استاد با کد استاد {professor_id} یافت نشد ', status_code=404)
    return result


@router.put("/v1/Update_professor/{professor_id}" , status_code=201)
def update_professor_API(professor_id:str , current_user: Annotated[str, Depends(authentication.get_current_professor)] ,professor_update:dict=Body() , db:Session=Depends(get_db)):
    id=P_crud.read_professor_ID(db=db, id=current_user['id']).user_professor_id
    if current_user['Role']!='professor' or professor_id!=id : raise HTTPException(detail='شما مجوز دسترسی به این بخش را ندارید', status_code=403)
    if P_crud.read_professor(db=db, p_id=professor_id)==None : raise HTTPException(detail=f'استاد با کد استاد {professor_id} یافت نشد ', status_code=404)
    else:
        selected_professor=P_crud.select_professor(db=db, id= professor_id)
        temp={**selected_professor, **professor_update}
        data = POR.Professor_Info_In(**temp)
        if data.user_professor_id!=professor_id and P_crud.read_professor(db=db, p_id=data.user_professor_id) : raise HTTPException(detail='کد استاد وارد شده نامعتر است', status_code=400)
        P_crud.update_professor(data=data , db=db,id=professor_id , lc= selected_professor['user_professor_course_IDs'])
    return 'اپدیت اطلاعات استاد موفقیت امیز بود'


@router.delete("/v1/Delete_professor/{professor_id}",status_code=200)
def delete_professor_API(professor_id:str , current_user: Annotated[str, Depends(authentication.get_current_professor)],db:Session=Depends(get_db)):
    id=P_crud.read_professor_ID(db=db, id=current_user['id']).user_professor_id
    if current_user['Role']!='professor' or professor_id!=id : raise HTTPException(detail='شما مجوز دسترسی به این بخش را ندارید', status_code=403)
    elif P_crud.read_professor(db=db, p_id=professor_id)==None : raise HTTPException(detail=f'استاد با کد استاد : {professor_id} یافت نشد ', status_code=404)
    P_crud.delete_professor(db=db , id=professor_id)
    return 'حذف اطلاعات استاد موفقیت امیز بود'

@router.delete("/v1/Delete_professor_course/{professor_id}/{course_id}",status_code=200)
def delete_professor_course_API(professor_id:str, course_id:str, current_user: Annotated[str, Depends(authentication.get_current_professor)], db:Session=Depends(get_db)):
    id=P_crud.read_professor_ID(db=db, id=current_user['id']).user_professor_id
    if current_user['Role']!='professor' or professor_id!=id : raise HTTPException(detail='شما مجوز دسترسی به این بخش را ندارید', status_code=403)
    if P_crud.read_professor(db=db, p_id=professor_id)==None : raise HTTPException(detail=f'استاد با کد استاد : {professor_id} یافت نشد ', status_code=404)
    P_crud.delete_professor_course(db=db, p_id=professor_id, c_id=course_id)
    return 'حذف اطلاعات درس استاد موفقیت امیز بود'






