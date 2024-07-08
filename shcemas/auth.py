from pydantic import BaseModel


class Admin (BaseModel):
    user_name : str
    user_admin_id : int


# class User_login (BaseModel):
#     Role : str
#     id : int
