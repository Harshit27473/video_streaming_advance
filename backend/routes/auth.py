from secret_keys import SecretKeys
from pydantic_models.auth_models import SignupRequest
from fastapi import APIRouter
import boto3


router = APIRouter()
secret_keys = SecretKeys()

COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
COGNITO_SECRET_KEY = secret_keys.COGNITO_CLIENT_SECRET
 

cognito_client = boto3.client("cognito-idp", region_name="ap-south-1")

@router.post("/signup")
def signup_user(data: SignupRequest):
    cognito_response =cognito_client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=data.email, 
        Password=data.password,
        UserAttributes=[
             {
                 'Name': "email", 'Value': data.email
             },
             {
                 'Name': "name", 'Value': data.name
             }
        ],
    )

    return cognito_response