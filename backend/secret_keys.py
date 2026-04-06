from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()  # Load environment variables from .env file

class SecretKeys(BaseSettings):
    COGNITO_CLIENT_ID: str = ""
    COGNITO_CLIENT_SECRET: str = ""
    REGION_NAME: str = ""
    DATABASE_URL: str = ""
    AWS_RAW_VIDEOS_BUCKET: str = ""
    AWS_VIDEOS_THUMBNAILS_BUCKET: str = ""


    
