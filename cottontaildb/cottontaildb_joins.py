#with CottontailDBClient('localhost', 1865) as client:
from cottontaildb_client import CottontailDBClient
from google.protobuf.json_format import MessageToDict
import pandas as pd


def cottontail_to_df(client):
    result = client.knn([1.3,1.3,4.7,2.4],"tal_db","color_sketch","sketch_vector", ["video_id", "keyframe_id", "distance"])
    test = MessageToDict(list(result)[0])

    response = {}

    columns = (test["columns"])
    results = test["tuples"]
    for i, tuple in enumerate(results):
        response[f"data_{i}"] = dict()
        response[f"data_{i}"][columns[0]["name"]] = tuple["data"][0]["doubleData"]
        response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
        response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]

    df = pd.DataFrame.from_dict(response)

    return df.T