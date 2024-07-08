from database import models 

def create_admin(db,data):
    db_admin= models.Admin(**data.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
def read_admin(db, id):
    return db.query(models.Admin).filter(models.Admin.user_admin_id == id).first()