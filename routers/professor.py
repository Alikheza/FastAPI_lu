from fastapi import APIRouter , Depends , HTTPException , Body
from sqlalchemy.orm import Session
from shcemas import professor as POR
from database.CRUD import professor as P_crud
from dependency import get_db
 
router = APIRouter()

@router.post("/Register_professor" , status_code=201)
def create_professor_API(professor_validation: POR.Professor_Info_In , db:Session=Depends(get_db)):
    if P_crud.read_professor(db=db, p_id=professor_validation.user_professor_id)!= None :
        raise HTTPException(detail='کد استاد وارد شده نمیتواند تکراری باشد', status_code=400)
    P_crud.create_professor(db=db , data= professor_validation)
    return 'ثبت اطلعات استاد موفقیت امیز بود'

@router.get("/Read_professor/{professor_id}" , response_model=POR.Professor_Info_Out , status_code=200)
def read_professor_API(professor_id:str ,db:Session=Depends(get_db)):
    if professor_id.isdigit()==False : raise HTTPException(detail='کد استاد وارد شده نامعتر است کد استاد فقط حاوی اعداد است', status_code=400)
    result = P_crud.read_professor(db=db, p_id=professor_id)
    if result==None :
        raise HTTPException(detail=f'استاد با کد استاد : {professor_id} یافت نشد ', status_code=404)
    return result


@router.put("/Update_professor/{professor_id}" , status_code=201)
def update_professor_API(professor_id:str , professor_update:dict=Body() , db:Session=Depends(get_db)):
    if professor_id.isdigit()==False : raise HTTPException(detail='کد استاد وارد شده نامعتر است کد استاد فقط حاوی اعداد است', status_code=400)
    elif P_crud.read_professor(db=db, p_id=professor_id)==None : raise HTTPException(detail=f'استاد با کد استاد : {professor_id} یافت نشد ', status_code=404)
    else:
        temp={**P_crud.select_professor(db=db, id= professor_id), **professor_update}
        data = POR.Professor_Info_In(**temp)
        P_crud.update_professor(data=data , db=db,id=professor_id)
    return 'اپدیت اطلعات استاد موفقیت امیز بود'


@router.delete("/Delete_professor/{professor_id}" , status_code=200)
def delete_professor_API(professor_id:str ,db:Session=Depends(get_db)):
    if professor_id.isdigit()==False : raise HTTPException(detail='کد استاد وارد شده نامعتر است کد استاد فقط حاوی اعداد است', status_code=400)
    elif P_crud.read_professor(db=db, p_id=professor_id)==None : raise HTTPException(detail=f'استاد با کد استاد : {professor_id} یافت نشد ', status_code=404)
    P_crud.delete_professor(db=db , id=professor_id)
    return 'حذف اطلعات استاد موفقیت امیز بود'