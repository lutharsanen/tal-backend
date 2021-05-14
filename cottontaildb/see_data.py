from cottontaildb_client import CottontailDBClient
from google.protobuf.json_format import MessageToDict
import pandas as pd


def cottontail_to_df(result,vector_name):
    test = MessageToDict(list(result)[0])

    response = {}

    columns = (test["columns"])
    results = test["tuples"]
    for i, tuple in enumerate(results):
        response[f"data_{i}"] = dict()
        response[f"data_{i}"][vector_name] = tuple["data"][0]["doubleData"]
        response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
        response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]

    df = pd.DataFrame.from_dict(response)

    return df.T



with CottontailDBClient('localhost', 1865) as client:

    #print(client.get_entity_details("tal_db", "color_sketch"))
    #print(client.get_entity_details("tal_db", "color_image"))
    #print(client.get_entity_details("tal_db", "object_sketch"))
    
    result_sketch = client.knn([1.3,1.3,4.7,2.4],"tal_db","color_sketch","sketch_vector", ["video_id", "keyframe_id", "distance"],500)
    df_sketch = cottontail_to_df(result_sketch, "sketch_vector")

    result_color = client.knn([32,23,250],"tal_db","color_sketch","color_vector", ["video_id", "keyframe_id", "distance"],500)

    df_color = cottontail_to_df(result_color, "color_vector")

    merged_df = pd.merge(df_sketch,df_color,on=['video_id',"keyframe_id"])

    merged_df["distance"] = 0.5 * merged_df["color_vector"] + 0.5 * merged_df["sketch_vector"]
    merged_df = merged_df.drop(['color_vector', 'sketch_vector'], axis=1).sort_values(by=['distance'])

    
    print(merged_df.head(10).to_dict(orient="records"))

    ########################################################