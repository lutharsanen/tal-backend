import os

def get_all_filesname(path):
    files = os.listdir(path)
    return files

def get_keyframe_id(filename, video_id,path):
    video_path = filename.replace(f"{path}/home/keyframes_filtered/","")
    keyframe_path = video_path.replace(video_id,"")
    keyframe_id = keyframe_path.replace(f"shot_","").replace(f"_RKF.png","")
    return keyframe_id