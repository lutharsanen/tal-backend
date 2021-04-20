from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Video(Base):
    __tablename__ = "video"

    # egal to video_id
    video_id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    vimeo_id = Column(Integer)


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    video_id = Column(String, ForeignKey("video.video_id"))


class Text(Base):
    __tablename__ = "text"

    id = Column(Integer, primary_key=True)
    keyframe_id = Column(String)
    text = Column(String)
    video_id = Column(String, ForeignKey("video.video_id"))
    start_frame = Column(Integer)
    start_time = Column(Float)
