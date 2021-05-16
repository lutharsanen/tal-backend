from typing import List, Optional
from pydantic import BaseModel


class SketchBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class RGB(BaseModel):
    red: int
    green: int
    blue: int


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

class ColorSketchInput(BaseModel):
    color: List[RGB]
    box: List[SketchBox]

class ColorInput(BaseModel):
    color_one: List[RGB]
    color_two: List[RGB]
    color_three: List[RGB]
    color_four: List[RGB]
    color_five: List[RGB]
    color_six: List[RGB]
    color_seven: List[RGB]
    color_eight: List[RGB]
    color_nine: List[RGB]
    color_ten: List[RGB]
    color_eleven: List[RGB]
    color_twelve: List[RGB]
    
class ObjectSketchInput(BaseModel):
    object: str
    sketch: List[float]

class Test(BaseModel):
    test: List[RGB]