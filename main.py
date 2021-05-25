from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

import schemas

from helper import stemming_algo, cottontail_to_df, cottontail_where_to_df, cottontail_object_number_search
import numpy as np
import pandas as pd

from cottontaildb.cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from google.protobuf.json_format import MessageToDict
import json

app = FastAPI()

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


@app.get("/api/searchByVideoText")
def get_text(text: str):
    text = stemming_algo(text)

    with CottontailDBClient('localhost', 1865) as client:
        result = client.select_where("tal_db","text_search", ["video_id", "tesseract_text", "keyframe_id"], "tesseract_text", [f"%{text}%"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
            response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]  
    return {"results": list(response.values())}


@app.get("/api/searchByDescription")
def get_text(text: str):
    text = stemming_algo(text)

    with CottontailDBClient('localhost', 1865) as client:
        result = client.select_where("tal_db","video_search", ["video_id","description"], "description", [f"%{text}%"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"] 
    return {"results": list(response.values())}


@app.get("/api/searchByTitle")
def get_text(text: str):
    text = stemming_algo(text)

    with CottontailDBClient('localhost', 1865) as client:
        result = client.select_where("tal_db","video_search", ["video_id","title"], "title", [f"%{text}%"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"] 
    return {"results": list(response.values())}

@app.get("/api/searchByTag")
def get_text(text: str):
    text = stemming_algo(text)

    with CottontailDBClient('localhost', 1865) as client:
        result = client.select_where("tal_db","video_tags", ["video_id","tags"], "tags", [f"%{text}%"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"] 
    return {"results": list(response.values())}

@app.get("/api/searchByImageCapture")
def get_text(text: str):
    text = stemming_algo(text)

    with CottontailDBClient('localhost', 1865) as client:
        result = client.select_where("tal_db","text_search", ["video_id","keyframe_id", "start_time","image_capture_text"], "image_capture_text", [f"%{text}%"])
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
            print(results)
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
            response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]
            response[f"{i}"][columns[3]["name"]] = tuple["data"][3]["floatData"]
    return {"results": list(response.values())}

################ Cottonttail API-Calls ############################

@app.post("/api/searchByColorSketch")
def get_sketch(request: schemas.ColorSketchInput):
    color_query = [request.color.red,request.color.green,request.color.blue]
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch_query = [request.box.x1,request.box.y1,request.box.x2,request.box.y2]
    object_query = request.object

    with CottontailDBClient('localhost', 1865) as client:
        result_sketch = client.knn_where(sketch_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object_query],2000)
        df_sketch = cottontail_where_to_df(result_sketch, "sketch_vector")
        print(df_sketch)
        result_color = client.knn(color_query,"tal_db","sketch","color_vector", ["box_id","video_id", "keyframe_id","start_time", "distance"],2000)
        df_color = cottontail_to_df(result_color, "color_vector")
        print(df_color)
        merged_df = pd.merge(df_sketch,df_color,on=['box_id','video_id',"keyframe_id","start_time"])
        merged_df["distance"] = 0.5 * merged_df["color_vector"] + 0.5 * merged_df["sketch_vector"]
        merged_df = merged_df.drop(['color_vector', 'sketch_vector'], axis=1).sort_values(by=['distance'])
        response = merged_df.drop_duplicates(subset=['box_id']).head(10).to_dict(orient="records")
        print(response)

    return {"results": response}

@app.post("/api/searchByTwoObjects")
def get_sketch(request: schemas.DoubleObjectSketchInput):
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch1_query = [request.sketch1.x1,request.sketch1.y1,request.sketch1.x2,request.sketch1.y2]
    object1_query = request.object1

    sketch2_query = [request.sketch2.x1,request.sketch2.y1,request.sketch2.x2,request.sketch2.y2]
    object2_query = request.object2

    with CottontailDBClient('localhost', 1865) as client:
        result1_sketch = client.knn_where(sketch1_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object1_query],2000)
        df_sketch1 = cottontail_where_to_df(result1_sketch, "sketch_vector")
        print(df_sketch1)
        result2_sketch = client.knn_where(sketch2_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object2_query],2000)
        df_sketch2 = cottontail_where_to_df(result2_sketch, "sketch_vector")
        print(df_sketch2)
        merged_df = pd.merge(df_sketch1,df_sketch2,on=['video_id',"keyframe_id","start_time"])
        print(merged_df)
        merged_df["distance"] = 0.5 * merged_df["sketch_vector_x"] + 0.5 * merged_df["sketch_vector_y"]
        merged_df = merged_df.drop(['sketch_vector_x','sketch_vector_y','object_x','object_y','box_id_x','box_id_y'], axis=1).sort_values(by=['distance'])
        response = merged_df.head(10).to_dict(orient="records")
        print(response)

    return {"results": response}


@app.post("/api/searchByThreeObjects")
def get_sketch(request: schemas.ThreeObjectSketchInput):
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch1_query = [request.sketch1.x1,request.sketch1.y1,request.sketch1.x2,request.sketch1.y2]
    object1_query = request.object1

    sketch2_query = [request.sketch2.x1,request.sketch2.y1,request.sketch2.x2,request.sketch2.y2]
    object2_query = request.object2

    sketch3_query = [request.sketch3.x1,request.sketch3.y1,request.sketch3.x2,request.sketch3.y2]
    object3_query = request.object3


    with CottontailDBClient('localhost', 1865) as client:
        result1_sketch = client.knn_where(sketch1_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object1_query],2000)
        df_sketch1 = cottontail_where_to_df(result1_sketch, "sketch_vector")
        print(df_sketch1)
        result2_sketch = client.knn_where(sketch2_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object2_query],2000)
        df_sketch2 = cottontail_where_to_df(result2_sketch, "sketch_vector")
        print(df_sketch2)

        result3_sketch = client.knn_where(sketch3_query,"tal_db","sketch","sketch_vector","object", ["box_id","video_id", "keyframe_id","start_time","object", "distance"],[object3_query],2000)
        df_sketch3 = cottontail_where_to_df(result3_sketch, "sketch_vector")
        print(df_sketch3)

        merged_df = df_sketch1.merge(df_sketch2,on=['video_id',"keyframe_id","start_time"]).merge(df_sketch3,on=['video_id',"keyframe_id","start_time"])
        print(merged_df)
        merged_df["distance"] = 1/3 * merged_df["sketch_vector_x"] + 1/3 * merged_df["sketch_vector_y"] + 1/3 * merged_df["sketch_vector"]
        merged_df = merged_df.drop(['sketch_vector_x','sketch_vector_y','sketch_vector','box_id_x','box_id_y','box_id'], axis=1).sort_values(by=['distance'])
        response = merged_df.head(10).to_dict(orient="records")
        print(response)

    return {"results": response}

@app.post("/api/searchByColor") 
def get_sketch(request: schemas.ColorInput):
    color_query = [
        request.c0.red,
        request.c0.green,
        request.c0.blue,
        request.c1.red,
        request.c1.green,
        request.c1.blue,
        request.c2.red,
        request.c2.green,
        request.c2.blue,
        request.c3.red,
        request.c3.green,
        request.c3.blue,
        request.c4.red,
        request.c4.green,
        request.c4.blue,
        request.c5.red,
        request.c5.green,
        request.c5.blue,
        request.c6.red,
        request.c6.green,
        request.c6.blue,
        request.c7.red,
        request.c7.green,
        request.c7.blue,
        request.c8.red,
        request.c8.green,
        request.c8.blue,
        request.c9.red,
        request.c9.green,
        request.c9.blue,
        request.c10.red,
        request.c10.green,
        request.c10.blue,
        request.c11.red,
        request.c11.green,
        request.c11.blue,
        ]

    with CottontailDBClient('localhost', 1865) as client:
        result = client.knn(color_query, "tal_db","color_image","dominant_color_vector", ["video_id", "keyframe_id", "start_time","distance"],500)
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["doubleData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
            response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]
            response[f"{i}"][columns[3]["name"]] = tuple["data"][3]["floatData"] 
    return {"results": list(response.values())}

@app.post("/api/searchByObjectSketch")
def get_sketch(request: schemas.ObjectSketchInput):
    object_query = request.object
    # (x1,y1) is lower left and (x2,y2) is upper right
    sketch_query = [request.sketch.x1,request.sketch.y1,request.sketch.x2,request.sketch.y2] # list of 4 elements
    
    with CottontailDBClient('localhost', 1865) as client:
        
        result = client.knn_where(sketch_query,"tal_db","sketch","sketch_vector","object", ["video_id", "keyframe_id", "distance", "object"],[object_query],200)
        result = MessageToDict(list(result)[0])
        response = {}
        columns = result["columns"]
        if 'tuples' in result.keys():
            results = result["tuples"]
        else:
            return {"results": []}
        for i, tuple in enumerate(results):
            response[f"{i}"] = dict()
            response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
            response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["doubleData"]
            response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["stringData"]
            response[f"{i}"][columns[3]["name"]] = tuple["data"][3]["intData"] 
            
    return {"results": list(response.values())}

@app.post("/api/searchByNumberObject")
def get_sketch(request: schemas.ObjectNumber):
    object_query = request.object
    # (x1,y1) is lower left and (x2,y2) is upper right
    number = request.number # list of 4 elements
    
    with CottontailDBClient('localhost', 1865) as client:
        
        result = client.select_where("tal_db","sketch",["box_id","video_id", "keyframe_id", "start_time","object"],"object", [request.object])
        response = cottontail_object_number_search(result, number)


    return {"results": response.to_dict(orient="records")}

##################### Simple Get-Request ###################################

@app.get("/api/getAllTags")
def all_tags():
    with CottontailDBClient('localhost', 1865) as client:
        result = client.select("tal_db","video_tags", ["tags"])
        result = MessageToDict(list(result)[0])
        response = []
        results = result["tuples"]
        for i, tuple in enumerate(results):
            response.append(tuple["data"][0]["stringData"])

    return {"results": response}

@app.get("/api/getAllColors")
def all_tags():
    COLORS = (
    (0,0,0), #black 
    (255,255,255), #white
    (255,0,0), #red
    (0,255,0), #lime
    (0,0,255), #blue
    (255,255,0), #yellow
    (0,255,255), #cyan
    (255,0,255), #magenta
    (192,192,192), #silver
    (128,128,128), #gray
    (128,0,0), #maroon
    (128,128,0), #olive
    (0,128,0), #green
    (128,0,128), #purple
    (0,128,128), #teal
    (0,0,128), #navy
    (255,165,0) #orange
)
    return {"results": COLORS}

@app.get("/api/getAllObjects")
def all_tags():
    with CottontailDBClient('localhost', 1865) as client:
        result = client.select("tal_db","sketch", ["object"])
        result = MessageToDict(list(result)[0])
        response = []
        results = result["tuples"]
        for tuple in results:
            response.append(tuple["data"][0]["stringData"])

    return {"results": response}


