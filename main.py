from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from helper import stemming_algo, cottontail_to_df, cottontail_where_to_df
import numpy as np
import pandas as pd

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


@app.post("/test")
def test_api(request: schemas.Test):
    lst = [request.test]
    return {"data": lst}

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

@app.post("/api/searchByColorSketch")
def get_sketch(request: schemas.ColorSketchInput):
    color_query = [request.color.red,request.color.green,request.color.blue]
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch_query = [request.box.x1,request.box.y1,request.box.x2,request.box.y2]
    object_query = request.object
    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        result_sketch = client.knn_where(sketch_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object_query])
                        #client.knn_where(sketch_query,"tal_db","sketch","sketch_vector","object", ["video_id", "keyframe_id", "distance", "object"],[object_query])
        df_sketch = cottontail_where_to_df(result_sketch, "sketch_vector")

        result_color = client.knn(color_query,"tal_db","sketch","color_vector", ["box_id","video_id", "keyframe_id","start_time", "distance"],500)

        df_color = cottontail_to_df(result_color, "color_vector")

        merged_df = pd.merge(df_sketch,df_color,on=['box_id','video_id',"keyframe_id","start_time"])

        merged_df["distance"] = 0.5 * merged_df["color_vector"] + 0.5 * merged_df["sketch_vector"]
        merged_df = merged_df.drop(['color_vector', 'sketch_vector'], axis=1).sort_values(by=['distance'])
    
        response = merged_df.drop_duplicates(subset=['box_id']).head(10).to_dict(orient="records")

    ########################################################
    return {"result": response}

@app.post("/api/searchByColor")
def get_sketch(request: schemas.ColorInput):
    color_query = [
        request._0.red,
        request._0.green,
        request._0.blue,
        request._1.red,
        request._1.green,
        request._1.blue,
        request._2.red,
        request._2.green,
        request._2.blue,
        request._3.red,
        request._3.green,
        request._3.blue,
        request._4.red,
        request._4.green,
        request._4.blue,
        request._5.red,
        request._5.green,
        request._5.blue,
        request._6.red,
        request._6.green,
        request._6.blue,
        request._7.red,
        request._7.green,
        request._7.blue,
        request._8.red,
        request._8.green,
        request._8.blue,
        request._9.red,
        request._9.green,
        request._9.blue,
        request._10.red,
        request._10.green,
        request._10.blue,
        request._11.red,
        request._11.green,
        request._11.blue,
        ]


    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        result = client.knn(color_query, "tal_db","color_image","dominant_color_vector", ["video_id", "keyframe_id", "start_time","distance"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        results = result["tuples"]
        for i, tuple in enumerate(results):
            response[f"data_{i}"] = dict()
            response[f"data_{i}"][columns[0]["name"]] = tuple["data"][0]["doubleData"]
            response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
            response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]
            response[f"data_{i}"][columns[3]["name"]] = tuple["data"][3]["intData"] 
    ########################################################
    return {"result": response}

@app.post("/api/searchByObjectSketch")
def get_sketch(request: schemas.ObjectSketchInput):
    object_query = request.object
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch_query = [request.sketch.x1,request.sketch.y1,request.sketch.x2,request.sketch.y2] # list of 4 elements
    
    ######### do some cottontail knn query #################
    with CottontailDBClient('localhost', 1865) as client:
        
        result = client.knn_where(sketch_query,"tal_db","sketch","sketch_vector","object", ["video_id", "keyframe_id", "distance", "object"],[object_query])
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

