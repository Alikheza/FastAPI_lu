from fastapi import FastAPI
from routers import  student , course , professor
from database.connect import create_all_table

app=FastAPI()

@app.on_event("startup")
def startup_event():
    create_all_table()

app.include_router(course.router, tags=["course"])
app.include_router(professor.router, tags=["professor"])
app.include_router(student.router, tags=["student"])
