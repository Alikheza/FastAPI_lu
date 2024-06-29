from pydantic_settings import BaseSettings


class ENV(BaseSettings):

    DATABASE_HOST : str 
    DATABASE_USERNAME : str 
    DATABASE_PASSWORD : str 
    DATABASE_PORT : str 
    DATABASE_NAME : str 

    class Config:
        env_file = ".env"


Evariable=ENV()