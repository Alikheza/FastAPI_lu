from fastapi import APIRouter , Depends , HTTPException ,Body
from sqlalchemy.orm import Session
from shcemas.auth import Admin
from app import dependency , authentication
from database.CRUD import admin as A_crud
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter()


@router.post("/v1/Register_admin" , status_code=201)
def create_admin_API(admin_validation: Admin , db:Session=Depends(dependency.get_db)):
    try:
        A_crud.create_admin(db=db , data=admin_validation)
    except:
        raise HTTPException(detail='ثبت ادمین موفقیت امیز نبود', status_code=400)
    return 'ثبت ادمین موفقیت امیز بود'

@router.get("/v1/Admin_read")
def login_admin_API( current_user: Annotated[str, Depends(authentication.get_current_admin)], db:Session=Depends(dependency.get_db)):
    result= A_crud.read_admin(db=db,id=current_user['id'])
    return result

@router.post("/v1/Admin_login")
def get_access_token_API(data: OAuth2PasswordRequestForm = Depends()):
    token = authentication.create_access_token(data=data)
    return {"access_token":token, "token_type":"bearer"}