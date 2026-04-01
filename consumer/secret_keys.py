from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()  # Load environment variables from .env file

class SecretKeys(BaseSettings):
    REGION_NAME: str = ""
    AWS_SQS_VIDEO_PROCESSING: str = ""
    

    
