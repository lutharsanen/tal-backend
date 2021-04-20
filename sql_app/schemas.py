from typing import List, Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    video_id: str
    description: str
    title: str
    vimeo_id: str


class Tags(BaseModel):
    video_id: str
    tag: str


class Text(BaseModel):
    keyframe_id: str
    text: str
    video_id: str
    start_frame: int
    start_time: float

    class Config:
        orm_mode = True


class TextInput(BaseModel):
    text: str
