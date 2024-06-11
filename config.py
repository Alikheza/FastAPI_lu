from fastapi import FastAPI
from routers import  student , course , professor
from database.connect import create_all_table

app=FastAPI()

@app.on_event("startup")
def startup_event():
    create_all_table()

app.include_router(course.router)
app.include_router(student.router)
app.include_router(professor.router)