import os
import json
import re
import pandas as pd
import requests

from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal
from tqdm import tqdm

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered"))[200:]

    for videonr in tqdm(video_filelist):
        try:
            f = open(f"{path}/info/{videonr}.json")
            data = json.load(f)
            
            with CottontailDBClient('localhost', 1865) as client:
                  
                entry = {
                    'video_id': Literal(stringData = videonr),
                    'vimeo_id': Literal(stringData = data["vimeoId"].lower()),
                    'title': Literal(stringData = data["title"].lower()),
                    'description': Literal(stringData = cleanhtml(data["description"]).lower())
                }
                client.insert('tal_db', 'video_search', entry)

                for tag in data["tags"]:
                    entry = {
                        'video_id': Literal(stringData = videonr),
                        'tags':Literal(stringData = tag.lower())            
                    }
                    client.insert('tal_db', 'video_tags', entry)
                            
        except OSError:
            continue
        except UnicodeDecodeError:
            continue
        except UnicodeEncodeError:
            continue
        except UnicodeError:
            continue

path = "Y:/TAL"

run(path)
