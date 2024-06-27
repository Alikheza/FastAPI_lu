from pydantic_settings import BaseSettings


class ENV(BaseSettings):

    DATABASE_HOST : str = "localhost"
    DATABASE_USERNAME : str = "postgres"
    DATABASE_PASSWORD : str = "postgres"
    DATABASE_PORT : str = "5432"
    DATABASE_NAME : str = "postgres"

    class Config:
        env_file = ".env"


Evariable=ENV()