
from db.models.user import User
from db.db import get_db
from helper.auth_helper import get_secret_hash
from secret_keys import SecretKeys
from pydantic_models.auth_models import SignupRequest
from fastapi import APIRouter, Depends, HTTPException
import boto3
from sqlalchemy.orm import Session


router = APIRouter()
secret_keys = SecretKeys()

COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
COGNITO_SECRET_KEY = secret_keys.COGNITO_CLIENT_SECRET
 

cognito_client = boto3.client("cognito-idp", region_name=secret_keys.REGION_NAME)

@router.post("/signup")
def signup_user(
    data: SignupRequest, 
    db: Session= Depends(get_db),
    ):
    try:
        secret_hash = get_secret_hash(data.email, COGNITO_CLIENT_ID, COGNITO_SECRET_KEY)

        cognito_response =cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email, 
            Password=data.password,
            SecretHash=secret_hash,
            UserAttributes=[
                {
                    'Name': "email", 'Value': data.email
                },
                {
                    'Name': "name", 'Value': data.name
                }
            ],
        )

        cognito_sub = cognito_response.get("UserSub")

        if not cognito_sub:
            raise HTTPException(400, 'cognito did not return a valid user_sub')
    
        new_user = User(
            name=data.name,
            email=data.email,
            cognito_sub=cognito_sub,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "signup successful. please confirm your email if required"}
    except Exception as e:
        raise HTTPException(400, f'cognito signup exception {e}')