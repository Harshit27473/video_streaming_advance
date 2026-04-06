from pydantic import BaseModel


class UploadMetadata(BaseModel):
    title: str
    description: str
    video_id: str
    video_s3_key: str 
    visibility: str
