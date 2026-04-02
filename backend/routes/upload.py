import boto3
import uuid
from fastapi import APIRouter, Depends, HTTPException
from db.middleware.auth_middleware import get_current_user
from secret_keys import SecretKeys

router = APIRouter()
secret_keys = SecretKeys()

s3_client = boto3.client("s3", region_name = secret_keys.REGION_NAME)

@router.get("/url")
def get_presigned_url(user=Depends(get_current_user)):
    try:
        video_id = f"videos/{user['sub']}/{uuid.uuid4()}"
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": secret_keys.AWS_RAW_VIDEOS_BUCKET,
                "Key": video_id,
                "ContentType": "video/mp4",
            
            }
        ) 

        return{
            "url": response,
            "video_id": video_id,

        }
    except Exception as e:
        raise HTTPException(500, str(e))
             