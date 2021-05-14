from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from helper import stemming_algo
import numpy as np

models.Base.metadata.create_all(bind=engine)

from cottontaildb.cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from google.protobuf.json_format import MessageToDict
import json

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse("/docs")


@app.get("/test")
def test_api(limit: int):
    return {"data": 2*limit}


@app.post("/api/updateVideo")
def text_analyzer(request: schemas.VideoBase, db: Session = Depends(get_db)):
    new_keyframe_video = models.Video(
        video_id=request.video_id, description=request.description, title=request.title, vimeo_id=request.vimeo_id)
    db.add(new_keyframe_video)
    db.commit()
    db.refresh(new_keyframe_video)
    return {"database_update": "success"}


@app.post("/api/updateTags")
def text_analyzer(request: schemas.Tags, db: Session = Depends(get_db)):
    new_tag = models.Tags(
        video_id=request.video_id, tag=request.tag)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return {"database_update": "success"}


@app.post("/api/updateTextanalysis")
def text_analyzer(request: schemas.Text, db: Session = Depends(get_db)):
    new_keyframe_text = models.Text(
        keyframe_id=request.keyframe_id,
        text=request.text,
        video_id=request.video_id,
        start_frame=request.start_frame,
        start_time=request.start_time)
    db.add(new_keyframe_text)
    db.commit()
    db.refresh(new_keyframe_text)
    return {"database_update": "success"}


@app.get("/api/all-text")
def get_text(db: Session = Depends(get_db)):
    video_searched = db.query(models.Text).all()
    return video_searched


@app.get("/api/all-tags")
def get_text(db: Session = Depends(get_db)):
    video_searched = db.query(models.Tags).all()
    return video_searched


@app.get("/api/all-video")
def get_text(db: Session = Depends(get_db)):
    video_searched = db.query(models.Video).all()
    return video_searched


@app.get("/api/searchByVideoText")
def get_text(text: str, db: Session = Depends(get_db)):
    text = stemming_algo(text)
    video_searched = db.query(models.Text).filter(
        models.Text.text.ilike(f'%{text}%')).all()
    return {"results": video_searched}


@app.get("/api/searchByDescription")
def get_text(text: str, db: Session = Depends(get_db)):
    text = stemming_algo(text)
    video_searched = db.query(models.Video).filter(
        models.Video.description.ilike(f'%{text}%')).all()
    return {"results": video_searched}


@app.get("/api/searchByTitle")
def get_text(text: str, db: Session = Depends(get_db)):
    text = stemming_algo(text)
    video_searched = db.query(models.Video).filter(
        models.Video.title.ilike(f'%{text}%')).all()
    return {"results": video_searched}


@app.get("/api/searchByTag")
def get_text(text: str, db: Session = Depends(get_db)):
    text = stemming_algo(text)
    video_searched = db.query(models.Tags).filter(
        models.Tags.tag.ilike(f'%{text}%')).all()
    return {"results": video_searched}

################ Cottonttail API-Calls ############################

@app.get("/api/searchByColorSketch")
def get_sketch(request: schemas.ColorSketchInput):
    color_query = np.array(request.color)
    sketch_query = np.array(request.sketch)
    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        result_color = client.knn(color_query, "tal_db","color_sketch","color_vector", ["id", "distance"])
        result_sketch = client.knn(sketch_query,"tal_db","color_sketch","sketch_vector", ["id", "distance"])
    ########################################################
    return {"result": "TAL"}

@app.get("/api/searchByColor")
def get_sketch(request: schemas.ColorInput):
    color_query = request.color
    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        result_color = client.knn(color_query, "tal_db","color_image","color_vector", ["id", "distance"])
    ########################################################
    return {"result": "TAL"}

@app.get("/api/searchByObjectSketch")
def get_sketch(object:str, x1: float, y1:float, x2:float, y2:float):
    object_query = object
    sketch_query = [x1,y1,x2,y2] # list of 4 elements
    
    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        
        result = client.knn_where(sketch_query,"tal_db","object_sketch","sketch_vector","object", ["video_id", "keyframe_id", "distance", "object"],[object_query])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        results = result["tuples"]
        for i, tuple in enumerate(results):
            response[f"data_{i}"] = dict()
            response[f"data_{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["doubleData"]
            response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["stringData"]
            response[f"data_{i}"][columns[3]["name"]] = tuple["data"][3]["intData"] 
            
    ########################################################
    return {"result": response}

