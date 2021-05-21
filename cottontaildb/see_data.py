from cottontaildb_client import CottontailDBClient
from google.protobuf.json_format import MessageToDict
import pandas as pd


with CottontailDBClient('localhost', 1865) as client:

    print(client.get_entity_details("tal_db", "sketch"))
    print(client.get_entity_details("tal_db", "color_image"))
    print(client.get_entity_details("tal_db", "text_search"))
    print(client.get_entity_details("tal_db", "video_tags"))
    
    result = client.select("tal_db", "color_image",["video_id", "keyframe_id"])
    result = MessageToDict(list(result)[0])
    print(result)