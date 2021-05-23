from cottontaildb_client import CottontailDBClient,column_def,Type,Literal
from google.protobuf.json_format import MessageToDict
import pandas as pd
from tqdm import tqdm


with CottontailDBClient('localhost', 1865) as client:

    # Define entity sketch columns
    count_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('object', Type.STRING, nullable=False),
        column_def('count', Type.INTEGER, nullable=False),
        column_def('start_time', Type.INTEGER, nullable=False)
    ]
    # Create entity color sketch
    client.create_entity('tal_db', 'object_count', count_columns)

    result = client.select('tal_db', 'sketch', ['keyframe_id', 'video_id','box_id','object','start_time'])
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
    with tqdm(total=result.shape[0]) as pbar: 
        for row in tqdm(result.iterrows()):
            pbar.update(1)
            entry = {
                'video_id': Literal(stringData = row[1]["video_id"]),
                'keyframe_id': Literal(intData=int(row[1]["keyframe_id"])),
                'object': Literal(stringData = row[1]["object"]),
                'count': Literal(intData = row[1]["count"]),
                'start_time':Literal(intData = int(row[1]["start_time"])),
            }
            client.insert('tal_db', 'object_count', entry)