from PIL import Image
import pytesseract as tess
import os
import json
import re
import pandas as pd
import requests

from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal
from tqdm import tqdm

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

#tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def get_all_filesname(path):
    files = os.listdir(path)
    return files

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def run(path):
    video_filelist = get_all_filesname(f"{path}/home/keyframes_filtered")[:5]

    for videonr in tqdm(video_filelist):
        #f = open(f"D:\\Video Retrieval System\\info\\{videonr}.json")
        f = open(f"{path}/home/info/{videonr}.json")
        data = json.load(f)

        with CottontailDBClient('localhost', 1865) as client:    
            entry = {
                'video_id': Literal(stringData = videonr),
                'title': Literal(stringData = data["title"]),
                'description': Literal(stringData = cleanhtml(data["description"]))
            }
            client.insert('tal_db', 'video_search', entry)

            for tag in data["tags"]:
                entry = {
                    'video_id': Literal(stringData = videonr),
                    'tags':Literal(stringData = tag)            
                }
                client.insert('tal_db', 'video_tags', entry)
            f = open(f"{path}/home/msb/{videonr}.tsv")
            start_time = pd.read_csv(f, delimiter="\t")

            for filename in tqdm(get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}")):
                keyframe_id = get_keyframe_id(filename, videonr,path)
                keyframe_nr = int(keyframe_id)-1
                image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
                with open(image,"rb") as file:
                    file_form = {"image": (image, file,"image/png")}
                    text_url = "http://localhost:5000/model/predict"
                    r = requests.post(url = text_url, files = file_form)
                    response = r.json()
                    capture_text = response["predictions"][0]["caption"]
                img = Image.open(image)
                text = tess.image_to_string(img).strip("\n\x0c")
                if text != (" " or "") and len(text) > 0:
                    text.replace("/n", " ")
                    entry = {
                        'video_id': Literal(stringData = videonr),
                        'keyframe_id': Literal(intData=int(keyframe_id)),
                        'tesseract_text': Literal(stringData = text),
                        'start_time':Literal(intData = int(start_time.iloc[keyframe_nr]["startframe"])),
                        'start_time':Literal(stringData = capture_text)
                    }
                    client.insert('tal_db', 'text_search', entry)

path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"
#path = "/media/lkunam/Elements/Video Retrieval System"

run(path)
