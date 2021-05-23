from cottontaildb_client import CottontailDBClient,column_def,Type,Literal
from google.protobuf.json_format import MessageToDict
import pandas as pd


with CottontailDBClient('localhost', 1865) as client:

    client.drop_entity("tal_db","object_count")
    """
    text_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('tesseract_text', Type.STRING, nullable=True),
        column_def('start_time', Type.INTEGER, nullable=False),
        column_def('image_capture_text', Type.STRING, nullable=True)
    ]
    client.create_entity('tal_db', 'text_search', text_columns)
    tag_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('tags', Type.STRING, nullable=False)
    ]
    client.create_entity('tal_db', 'video_tags', tag_columns)
    video_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('title', Type.STRING, nullable=False),
        column_def('description', Type.STRING, nullable=False)
    ]
    client.create_entity('tal_db', 'video_search', video_columns)
    """
    #print(client.get_entity_details("tal_db", "sketch"))
    #print(client.get_entity_details("tal_db", "color_image"))
    #print(client.get_entity_details("tal_db", "text_search"))
    #print(client.get_entity_details("tal_db", "video_tags"))
    #print(client.get_entity_details("tal_db", "video_search"))
    #print(client.get_entity_details("tal_db", "video_search"))
    
    result = client.select("tal_db", "text_search",["video_id", "keyframe_id", "image_capture_text"])
    #result = client.knn([0,0,0,0], "tal_db","color_image", "dominant_color_vector", ["video_id", "keyframe_id", "start_time","distance"])
    #result = MessageToDict(list(result)[0])

    #print(result)
    