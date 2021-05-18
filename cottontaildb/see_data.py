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

    result = client.select_where("tal_db","video_tags", ["video_id","tags"], "tags", ["nomod"])
    #result = client.select("tal_db","video_tags", ["video_id", "tags"])
    test = MessageToDict(list(result)[0])
    print(test)