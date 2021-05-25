from cottontaildb_client import CottontailDBClient,column_def,Type,Literal
from google.protobuf.json_format import MessageToDict
import pandas as pd


with CottontailDBClient('localhost', 1865) as client:

    #client.drop_schema("tal_db")
    #client.drop_entity("tal_db","transcription")
    #client.drop_entity("tal_db","video_search")
    #client.drop_entity("tal_db","video_tags")
    #print(client.list_entities("tal_db"))

    print(client.get_entity_details("tal_db", "sketch"))
    #print(client.get_entity_details("tal_db", "color_image_test"))
    #print(client.get_entity_details("tal_db", "text_search"))
    #print(client.get_entity_details("tal_db", "video_tags"))
    #print(client.get_entity_details("tal_db", "video_search"))
    
    result = client.select("tal_db", "sketch", ["video_id", "keyframe_id", "object", "start_time"])
    #result = client.select("tal_db", "color_image", ["video_id", "keyframe_id"])
    #result = client.knn([0,0,0,0], "tal_db","color_image", "dominant_color_vector", ["video_id", "keyframe_id", "start_time","distance"])
    result = MessageToDict(list(result)[0])

    print(result)