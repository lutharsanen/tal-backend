from typing import List, Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    video_id: int
    description: str
    title: str
    vimeo_id: str


class Tags(BaseModel):
    video_id: int
    tag: int


class Text(BaseModel):
    keyframe_id: str
    text: str
    video_id: int

    class Config:
        orm_mode = True


class TextInput(BaseModel):
    text: str
