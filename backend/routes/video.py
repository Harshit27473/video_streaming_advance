import json
from operator import or_
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models.video import ProcessingStatus, Video, VisibilityStatus
from db.middleware.auth_middleware import get_current_user
from db.db import get_db
from db.redis_db import redis_client

router = APIRouter()

@router.get("/all")
def get_all_videos (
    db: Session = Depends(get_db), 
    user=Depends(
        get_current_user,
        ),
):
    
    all_videos = db.query(Video).filter(
        Video.is_processing == ProcessingStatus.COMPLETED, 
        Video.visibility == VisibilityStatus.PUBLIC,
        ).all()
    
    return all_videos


@router.get("/")
def get_video_info (
    video_id: str, 
    db: Session = Depends(get_db), 
    user=Depends(
        get_current_user,
        ),
):
    cache_key = f"video_info:{video_id} "
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)
    video = (
        db.query(Video).filter(
        Video.id == video_id,
        Video.is_processing == ProcessingStatus.COMPLETED, 
        or_(
        Video.visibility == VisibilityStatus.PUBLIC,
        Video.visibility == VisibilityStatus.UNLISTED,
        ),
        )
       .first()
    )
    print(video.to_dict())
    redis_client.setex(cache_key, 3600, json.dumps(video.to_dict()))
    return video