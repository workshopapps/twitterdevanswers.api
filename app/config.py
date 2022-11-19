
from dotenv import load_dotenv
import os
from pydantic import BaseSettings
load_dotenv()


class Settings(BaseSettings):
    database_hostname = os.environ.get('DATABASE_HOSTNAME')
    database_port = os.environ.get('DATABASE_PORT')
    database_password = os.environ.get('DATABASE_PASSWORD')
    database_name = os.environ.get('DATABASE_USERNAME')
    database_username = os.environ.get('DATABASE_USERNAME')
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    test_database_username: str
    test_database_password: str
    test_database_hostname: str
    test_database_port: str
    test_database_name: str
    app_passwd: str

    class config:
        env_file = '.env'


settings = Settings()
