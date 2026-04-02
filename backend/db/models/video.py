from sqlalchemy import TEXT, Column , Integer , ForeignKey , Enum
import enum
from db.base import Base

class VisibilityStatus(enum.Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    UNLISTED = "UNLISTED"

class ProcessingStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"  

class Video(Base):
    __tablename__ = "videos"

    id = Column(TEXT, primary_key=True)
    title = Column(TEXT)
    description = Column(TEXT)
    User_id = Column(TEXT, ForeignKey("users.id"))
    video_s3_key = Column(TEXT)
    visibility = Column(
        Enum(VisibilityStatus),
        nullable=False, 
        default=VisibilityStatus.PRIVATE
    )
    is_processing = Column(
        Enum(ProcessingStatus), 
        nullable=False, 
        default=ProcessingStatus.IN_PROGRESS
    )
  