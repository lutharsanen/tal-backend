from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    description = Column(String)


class Text(Base):
    __tablename__ = "text"

    keyframe_id = Column(String, primary_key=True)
    text = Column(String)
    video_id = Column(Integer, ForeignKey("video.id"))
