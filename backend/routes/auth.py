
from db.models.user import User
from db.db import get_db
from helper.auth_helper import get_secret_hash
from secret_keys import SecretKeys
from pydantic_models.auth_models import LoginRequest, SignupRequest, confirmSignupRequest
from fastapi import APIRouter, Depends, HTTPException, Response
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

        return {"message": "signup successful. please confirm your email if required"}
    except Exception as e:
        raise HTTPException(400, f'cognito signup exception {e}')
    

@router.post("/login")
def login_user(
    data: LoginRequest, 
    response: Response,
    ):
    try:
        secret_hash = get_secret_hash(data.email, COGNITO_CLIENT_ID, COGNITO_SECRET_KEY)

        cognito_response =cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters=
               {
                   "USERNAME": data.email,
                   "PASSWORD": data.password,
                   "SECRET_HASH": secret_hash
               },       
        )
        auth_result = cognito_response.get("AuthenticationResult")
        if not auth_result:
            raise HTTPException(400, 'cognito did not return authentication result')

        access_token = auth_result.get("AccessToken")
        refresh_token = auth_result.get("RefreshToken")

        response.set_cookie(
            key="access_token", 
            value=access_token, 
            httponly=True, 
            secure= True
            )
        
        response.set_cookie(
            key="refresh_token", 
            value=refresh_token, 
            httponly=True, 
            secure= True
            )
        
        return {"message": "user confirmed successfully"}
    except Exception as e:
        raise HTTPException(400, f'cognito login exception {e}')
    
@router.post("/confirm-signup")
def confirm_signup(
    data: confirmSignupRequest,  
    ):
    try:
        secret_hash = get_secret_hash(data.email, COGNITO_CLIENT_ID, COGNITO_SECRET_KEY)

        cognito_response =cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            username=data.email,
            ConfirmationCode=data.otp,
            SecretHash=secret_hash,   
        )
        return {"message": "user confirmed successfully"}
    except Exception as e:
        raise HTTPException(400, f'cognito login exception {e}')