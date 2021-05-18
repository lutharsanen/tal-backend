from cottontaildb_client import CottontailDBClient
from google.protobuf.json_format import MessageToDict
import pandas as pd


with CottontailDBClient('localhost', 1865) as client:

    #print(client.get_entity_details("tal_db", "sketch"))
    #print(client.get_entity_details("tal_db", "color_image"))
    #print(client.get_entity_details("tal_db", "text_search"))
    #print(client.get_entity_details("tal_db", "video_tags"))
    
    #result_sketch = client.knn([200.3,200.32,200.7,200.4],"tal_db","object_sketch","sketch_vector", ["video_id", "keyframe_id", "distance","object"],100)
    #df_sketch = cottontail_to_df(result_sketch, "sketch_vector")
    #print(df_sketch)

    #print(MessageToDict(list(result_sketch)[0]))

    #result_color = client.knn([32,23,250],"tal_db","color_sketch","color_vector", ["video_id", "keyframe_id", "distance"],200)

    #df_color = cottontail_to_df(result_color, "color_vector")

    #print(df_color)

    #merged_df = df_sketch.merge(df_color,how="inner",on=["video_id","keyframe_id"])

    #merged_df["distance"] = 0.5 * merged_df["color_vector"] + 0.5 * merged_df["sketch_vector"]
    #merged_df = merged_df.drop(['color_vector', 'sketch_vector'], axis=1).sort_values(by=['distance'])

    #print(merged_df)
    #print(merged_df.head(10).to_dict(orient="records"))

    ########################################################

    #result = client.select("tal_db","video_tags", ["tags"])
    #result = client.select("tal_db","video_tags", ["video_id", "tags"])
    #test = MessageToDict(list(result)[0])
    #print(test)

    result = client.select_where("tal_db","sketch",["box_id","video_id", "keyframe_id", "start_time","object"],"object", ["person"])
    result = MessageToDict(list(result)[0])
    response = {}
    columns = result["columns"]
    results = result["tuples"]

    for i, tuple in enumerate(results):
        response[f"{i}"] = dict()
        response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
        response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["intData"] 
        response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["stringData"]
        response[f"{i}"][columns[3]["name"]] = tuple["data"][3]["intData"] 
        response[f"{i}"][columns[4]["name"]] = tuple["data"][4]["intData"] 


    df = pd.DataFrame.from_dict(response)

    df_t = df.T

    df_t=df_t.drop_duplicates(['box_id'])
    df_new = df_t.groupby(['keyframe_id', 'video_id']).size().reset_index(name="count")

    result = df_new[df_new["count"] > 2].sort_values(by=['count'],ascending=False)
    #df_new = df.T.groupby(['keyframe_id', 'video_id']).count()
    print(result)