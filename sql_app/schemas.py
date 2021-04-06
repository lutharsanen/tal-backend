from typing import List, Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    video_id: int
    description: str


class Text(BaseModel):
    keyframe_id: str
    text: str
    video_id: int

    class Config:
        orm_mode = True


class TextInput(BaseModel):
    text: str
