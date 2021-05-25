import os

from cottontail_helper import get_all_filesname
from cottontaildb_client import CottontailDBClient, Literal
from tqdm import tqdm


def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/videos"))[:10]
    
    for videonr in tqdm(video_filelist):
        try:
            for filename in tqdm(get_all_filesname(f"{path}/videos/{videonr}/")):
                    if filename.endswith(".txt"):
                        with open(f"{path}/videos/{videonr}/{filename}") as f:
                            data = f.readlines()
                            data = "".join(data).lower()
                            with CottontailDBClient('localhost', 1865) as client: 
                                entry = {
                                    'video_id': Literal(stringData = videonr),
                                    'audio_transcription': Literal(stringData = data)
                                    }
                                client.insert('tal_db', 'transcription', entry)
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