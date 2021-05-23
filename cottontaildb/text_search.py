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

tess.pytesseract.tesseract_cmd = r"C:\Users\fabia\Desktop\SOLIDWORKS_2016_SP5.0\inspection\CommonAppData\SOLIDWORKS\SOLIDWORKS Inspection 2016 Standalone\TrainableOCR\tesseract.exe"

def get_all_filesname(path):
    files = os.listdir(path)
    return files

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered"))[86:]
    
    for videonr in tqdm(video_filelist):
        #f = open(f"D:\\Video Retrieval System\\info\\{videonr}.json")
        try:
            f = open(f"{path}/info/{videonr}.json")
            data = json.load(f)

            with CottontailDBClient('localhost', 1865) as client:    
                entry = {
                    'video_id': Literal(stringData = videonr),
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
                f = open(f"{path}/msb/{videonr}.tsv")
                start_time = pd.read_csv(f, delimiter="\t")

                for filename in tqdm(get_all_filesname(f"{path}/keyframes_filtered/{videonr}")):
                    if filename != "Thumbs.db" and filename!= ".DAV":
                        keyframe_id = get_keyframe_id(filename, videonr,path)
                        keyframe_nr = int(keyframe_id)-1
                        image = f"{path}/keyframes_filtered/{videonr}/{filename}"
                        with open(image,"rb") as file:
                            file_form = {"image": (image, file,"image/png")}
                            text_url = "http://localhost:5000/model/predict"
                            r = requests.post(url = text_url, files = file_form)
                            response = r.json()
                            capture_text = response["predictions"][0]["caption"].lower()
                        img = Image.open(image)
                        text = tess.image_to_string(img).strip("\n\x0c")
                        if text != (" " or "") and len(text) > 0:
                            text = text.replace("/n", " ").lower()
                            entry = {
                                'video_id': Literal(stringData = videonr),
                                'keyframe_id': Literal(intData=int(keyframe_id)),
                                'tesseract_text': Literal(stringData = text),
                                'start_time':Literal(intData = int(start_time.iloc[keyframe_nr]["startframe"])),
                                'image_capture_text':Literal(stringData = capture_text)
                            }
                            client.insert('tal_db', 'text_search', entry)
        except OSError:
            continue
        except UnicodeDecodeError:
            continue
        except UnicodeEncodeError:
            continue
        except UnicodeError:
            continue

#path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"
#path = "/media/lkunam/Elements/Video Retrieval System"
path = "Y:/TAL"
run(path)
