from fastapi import APIRouter , Depends
from shcemas import student , professor
from sqlalchemy.orm import Session 
from database import course_module
from shcemas.course import Course_Info_In  , Course_Info_Out
from database.connect import  engine
from database.CRUD.course import create_course ,read_course

from dependency import get_db

router = APIRouter()

course_module.Base.metadata.create_all(bind=engine)

@router.post('/')
def test (Student:student.Student_Info):
    return Student
@router.post('/testp')
def testt (profesor:professor.Professor_Info):
    return profesor

@router.post("/test2")
def create_course_API( course:Course_Info_In, db:Session = Depends(get_db)):
    return create_course(db=db, course=course)

@router.get("/test3/{c_id}", response_model=Course_Info_Out )
def read_course_API(c_id:int,db:Session = Depends(get_db)):
    return read_course(db=db,id=c_id)