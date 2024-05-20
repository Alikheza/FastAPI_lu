from fastapi import APIRouter
from shcemas.student import Student_Info

router = APIRouter()

@router.post('/')
def test (Student_Info):
    return Student_Info