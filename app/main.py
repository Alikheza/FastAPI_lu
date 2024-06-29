from fastapi import FastAPI
from routers import  student , course , professor
from database.connect import create_all_table


def lifespan(app:FastAPI):
    try :
        create_all_table()
    except :
        raise Exception('DB IS NOT  WORKING PROPERLY')
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(course.router, tags=["course"])
app.include_router(professor.router, tags=["professor"])
app.include_router(student.router, tags=["student"])
