import jwt
from typing import Annotated
from jwt.exceptions import  ExpiredSignatureError
from datetime import datetime, timedelta ,timezone
from fastapi import status, HTTPException ,Depends 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import Evariable
from app.dependency import get_db
from database.CRUD import admin , professor , student


oauth2_admin = OAuth2PasswordBearer(tokenUrl='/v1/Admin_login',scheme_name="admin_login")
oauth2_professor = OAuth2PasswordBearer(tokenUrl='/v1/professor_login',scheme_name="professor_login")
oauth2_student = OAuth2PasswordBearer(tokenUrl='/v1/Student_login',scheme_name="student_login")

SECRET_KEY = Evariable.SECRET_KEY
ALGORITHM = Evariable.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Evariable.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data):
    data = {"Role":data.username, "id":data.password}
    encode= data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, t_exception , t_exception2,db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        Role = payload.get("Role")
        id = payload.get("id")
        if Role == 'admin':
            if admin.read_admin(db ,id) == None:
                raise t_exception
        elif Role == 'professor':
            if professor.read_professor_ID(db,id) == None:
                raise t_exception
        elif Role == 'student': 
            if student.read_student_ID_(db,id) == None:
                raise t_exception
    except ExpiredSignatureError:
        raise t_exception2
    except Exception:
        raise t_exception

    return {"Role":Role, "id":id}


def get_current_admin(token: Annotated[str, Depends(oauth2_admin)], db:Session=Depends(get_db)):
    t_exception = HTTPException(status_code=401,detail=f"توکن نامعتبر است", headers={"WWW-Authenticate": "Bearer"})
    t_exception2 = HTTPException(status_code=401, detail=f"توکن منقضی شده است", headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, t_exception, t_exception2 ,db )

def get_current_professor(token: Annotated[str, Depends(oauth2_professor)], db:Session=Depends(get_db)):
    t_exception = HTTPException(status_code=401, detail=f"توکن نامعتبر است", headers={"WWW-Authenticate": "Bearer"})
    t_exception2 = HTTPException(status_code=401, detail=f"توکن منقضی شده است", headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, t_exception, t_exception2, db)

def get_current_student(token: Annotated[str, Depends(oauth2_student)], db:Session=Depends(get_db)):
    t_exception = HTTPException(status_code=401, detail=f"توکن نامعتبر است", headers={"WWW-Authenticate": "Bearer"})
    t_exception2 = HTTPException(status_code=401, detail=f"توکن منقضی شده است", headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, t_exception, t_exception2, db)