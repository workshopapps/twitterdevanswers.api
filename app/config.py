
from dotenv import load_dotenv
from pydantic import BaseSettings
load_dotenv()


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    app_passwd: str
    test_database_username: str
    test_database_password: str
    test_database_hostname: str
    test_database_port: str
    test_database_name: str

    class config:
        env_file = '.env'


settings = Settings()
