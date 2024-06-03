from fastapi import APIRouter , Depends
from shcemas import student as S 
from shcemas import professor as P
from sqlalchemy.orm import Session 
from database import module
from shcemas.course import Course_Info_In  , Course_Info_Out
from database.connect import  engine
from database.CRUD import course , student , professor


from dependency import get_db

router = APIRouter()

module.Base.metadata.create_all(bind=engine)

@router.post('/')
def test (Student:S.Student_Info):
    return Student
@router.post('/testp')
def testt (profesor:P.Professor_Info_In):
    return profesor

@router.post("/test2")
def create_course_API( course:Course_Info_In, db:Session = Depends(get_db)):
    return course.create_course(db=db, course=course)

@router.get("/test3/{c_id}", response_model=Course_Info_Out)
def read_course_API(c_id:int,db:Session = Depends(get_db)):
    return course.read_course(db=db,id=c_id)

@router.post("/testpc")
def create_professor_API(data_create:P.Professor_Info_In,db:Session=Depends(get_db)):
    return professor.professor(db=db,data=data_create)
@router.post('/testS')
def create_student_API(data:S.Student_Info , db :Session=Depends(get_db)):
    return student.student(db=db , data=data)