from fastapi import APIRouter
from shcemas.student import Student_Check

router = APIRouter()

@router.post('/')
def test (Student_check):
    return Student_Check