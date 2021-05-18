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
    color: RGB
    box: SketchBox
    object: str

class ColorInput(BaseModel):
    _0: RGB
    _1: RGB
    _2: RGB
    _3: RGB
    _4: RGB
    _5: RGB
    _6: RGB
    _7: RGB
    _8: RGB
    _9: RGB
    _10: RGB
    _11: RGB
    
class ObjectSketchInput(BaseModel):
    object: str
    sketch: SketchBox

class Test(BaseModel):
    test: RGB