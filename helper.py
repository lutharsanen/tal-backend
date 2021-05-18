from nltk.stem import PorterStemmer
from google.protobuf.json_format import MessageToDict
import pandas as pd

################### helper-function ################


def stemming_algo(word):
    ps = PorterStemmer()
    stemmed_word = ps.stem(word)
    return stemmed_word

def cottontail_to_df(result,vector_name):
    test = MessageToDict(list(result)[0])
    response = {}

    columns = test["columns"]
    results = test["tuples"]
    #print(result)
    for i, tuple in enumerate(results):
        response[f"data_{i}"] = dict()
        response[f"data_{i}"][vector_name] = tuple["data"][0]["doubleData"]
        response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["intData"]
        response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["stringData"]
        response[f"data_{i}"][columns[3]["name"]] = tuple["data"][3]["intData"]
        response[f"data_{i}"][columns[4]["name"]] = tuple["data"][4]["intData"]

    df = pd.DataFrame.from_dict(response)

    return df.T


def cottontail_where_to_df(result,vector_name):
    test = MessageToDict(list(result)[0])
    response = {}

    columns = test["columns"]
    results = test["tuples"]
    for i, tuple in enumerate(results):
        response[f"data_{i}"] = dict()
        response[f"data_{i}"][columns[0]["name"]] = tuple["data"][0]["stringData"]
        response[f"data_{i}"][vector_name] = tuple["data"][1]["doubleData"]
        response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]
        response[f"data_{i}"][columns[3]["name"]] = tuple["data"][3]["stringData"]
        response[f"data_{i}"][columns[4]["name"]] = tuple["data"][4]["intData"]
        response[f"data_{i}"][columns[5]["name"]] = tuple["data"][5]["intData"]

    df = pd.DataFrame.from_dict(response)

    return df.T


def cottontail_object_number_search(result,count):
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
    df_new = df_t.groupby(['keyframe_id', 'video_id','start_time']).size().reset_index(name="count")

    result = df_new[df_new["count"] >= count].sort_values(by=['count'],ascending=False)

    return result