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
    for i, tuple in enumerate(results):
        response[f"data_{i}"] = dict()
        response[f"data_{i}"][vector_name] = tuple["data"][0]["doubleData"]
        response[f"data_{i}"][columns[1]["name"]] = tuple["data"][1]["stringData"]
        response[f"data_{i}"][columns[2]["name"]] = tuple["data"][2]["intData"]

    df = pd.DataFrame.from_dict(response)

    return df.T