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
    max_results: int

class ColorInput(BaseModel):
    c0: RGB
    c1: RGB
    c2: RGB
    c3: RGB
    c4: RGB
    c5: RGB
    c6: RGB
    c7: RGB
    c8: RGB
    c9: RGB
    c10: RGB
    c11: RGB
    max_results: int
    
class ObjectSketchInput(BaseModel):
    object: str
    sketch: SketchBox
    max_results: int

class DoubleObjectSketchInput(BaseModel):
    object1: str
    sketch1: SketchBox
    object2: str
    sketch2: SketchBox
    max_results: int

class ThreeObjectSketchInput(BaseModel):
    object1: str
    sketch1: SketchBox
    object2: str
    sketch2: SketchBox
    object3: str
    sketch3: SketchBox
    max_results: int


class Test(BaseModel):
    test: RGB

class ObjectNumber(BaseModel):
    object: str
    number: int