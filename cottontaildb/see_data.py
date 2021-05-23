from cottontaildb_client import CottontailDBClient,column_def,Type,Literal
from google.protobuf.json_format import MessageToDict
import pandas as pd


with CottontailDBClient('localhost', 1865) as client:
    """
    client.drop_entity("tal_db","text_search")
    client.drop_entity("tal_db","video_search")
    client.drop_entity("tal_db","video_tags")
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
    result = MessageToDict(list(result)[0])

    print(result)
    
    """

    # Define entity tag columns
    test_columns = [
        column_def('test', Type.INTEGER, nullable=False),
        column_def('test_value', Type.INTEGER, nullable=False)
    ]

    # Create entity feature vector
    client.create_entity('tal_db', 'test', test_columns)

    columns = ['test', 'test_value']
    
    values = [
        [Literal(stringData='test_10'), Literal(intData=10)],
        [Literal(stringData='test_20'), Literal(intData=20)]
    ]

    client.insert_batch('tal_db', 'test', columns, values)
    result = client.select('tal_db', 'test', ['test', 'test_value'])
    result = MessageToDict(list(result)[0])

    response = {}
    columns = result["columns"]
    results = result["tuples"]

    for i, tuple in enumerate(results):
        response[f"{i}"] = dict()
        response[f"{i}"][columns[0]["name"]] = tuple["data"][0]["intData"]
        response[f"{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
        response[f"{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]
        response[f"{i}"][columns[3]["name"]] = tuple["data"][3]["stringData"]
        response[f"{i}"][columns[4]["name"]] = tuple["data"][4]["intData"]


    df = pd.DataFrame.from_dict(response)

    df_t = df.T

    df_t=df_t.drop_duplicates(['box_id'])
    df_new = df_t.groupby(['keyframe_id', 'video_id','object','start_time']).size().reset_index(name="count")

    result = df_new[df_new["count"] >= 2].sort_values(by=['count'],ascending=False)
    """
