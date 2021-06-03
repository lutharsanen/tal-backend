from cottontaildb_client import CottontailDBClient,column_def,Type,Literal
from google.protobuf.json_format import MessageToDict
import pandas as pd
from tqdm import tqdm


with CottontailDBClient('localhost', 1865) as client:

    
    sketch_details = client.get_entity_details("tal_db", "sketch")
    row_iterations = sketch_details["rows"]//100000
    mod = sketch_details["rows"] % 100000

    response = {}
    counter = 0

    for i in range(row_iterations):
        start_point = i*100000
        end_point = (i+1)*100000 -1
        print(start_point, end_point)

        result = client.limited_select('tal_db', 'sketch', ['keyframe_id', 'video_id','box_id','object','start_time'], start_point, end_point)
        result = MessageToDict(list(result)[0])

        columns = result["columns"]
        results = result["tuples"]

        for tuple in results:
            response[f"{counter}"] = dict()
            response[f"{counter}"][columns[0]["name"]] = tuple["data"][0]["intData"]
            response[f"{counter}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
            response[f"{counter}"][columns[2]["name"]] = tuple["data"][2]["intData"]
            response[f"{counter}"][columns[3]["name"]] = tuple["data"][3]["stringData"]
            response[f"{counter}"][columns[4]["name"]] = tuple["data"][4]["floatData"]

            counter += 1

    last_start = sketch_details["rows"]//100000*100000
    last_end = sketch_details["rows"]//100000*100000 + mod

    print(last_start, last_end)

    result = client.limited_select('tal_db', 'sketch', ['keyframe_id', 'video_id','box_id','object','start_time'], last_start, last_end)
    result = MessageToDict(list(result)[0])

    columns = result["columns"]
    results = result["tuples"]

    for tuple in results:
        response[f"{counter}"] = dict()
        response[f"{counter}"][columns[0]["name"]] = tuple["data"][0]["intData"]
        response[f"{counter}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
        response[f"{counter}"][columns[2]["name"]] = tuple["data"][2]["intData"]
        response[f"{counter}"][columns[3]["name"]] = tuple["data"][3]["stringData"]
        response[f"{counter}"][columns[4]["name"]] = tuple["data"][4]["floatData"]

        counter += 1


    df = pd.DataFrame.from_dict(response)

    df_t = df.T

    print(df_t)

    df_t=df_t.drop_duplicates(['box_id'])
    df_new = df_t.groupby(['keyframe_id', 'video_id','object','start_time']).size().reset_index(name="count")

    result = df_new[df_new["count"] >= 1].sort_values(by=['count'],ascending=False)
    print(result)
    with tqdm(total=result.shape[0]) as pbar: 
        for row in tqdm(result.iterrows()):
            pbar.update(1)
            entry = {
                'video_id': Literal(stringData = row[1]["video_id"]),
                'keyframe_id': Literal(intData=int(row[1]["keyframe_id"])),
                'object': Literal(stringData = row[1]["object"]),
                'count': Literal(intData = row[1]["count"]),
                'start_time':Literal(floatData = float(row[1]["start_time"])),
            }
            client.insert('tal_db', 'object_count', entry)