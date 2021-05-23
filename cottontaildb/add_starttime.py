import pytesseract as tess
import os
import pandas as pd

from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal
from tqdm import tqdm

def get_all_filesname(path):
    files = os.listdir(path)
    return files

# TEXT SEARCH
def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered"))[86:]

    for videonr in tqdm(video_filelist):
        f = open(f"{path}/msb/{videonr}.tsv")
        msb = pd.read_csv(f, delimiter="\t")       
        try:
            for filename in tqdm(get_all_filesname(f"{path}/keyframes_filtered/{videonr}")):   
                if filename != "Thumbs.db" and filename!= ".DAV":
                    keyframe_id = get_keyframe_id(filename, videonr,path)
                    keyframe_nr = int(keyframe_id)-1
                    
                    with CottontailDBClient('localhost', 1865) as client: 
                        entry = {
                            'start_time_2': Literal(intData = int(msb.iloc[keyframe_nr]["starttime"])),
                        }
                        client.insert('tal_db', 'text_search', entry)
                        #client.insert('tal_db', 'color_image', entry)
                        #client.insert('tal_db', 'sketch', entry)


            
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
