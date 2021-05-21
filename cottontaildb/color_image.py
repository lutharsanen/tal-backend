# import some common libraries
from PIL import Image
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector
import os
import multiprocessing
from multiprocessing import Process
import numpy as np
from math import sqrt
from tqdm import tqdm
import pandas as pd


COLORS = (
    (0,0,0), #black 
    (255,255,255), #white
    (255,0,0), #red
    (0,255,0), #lime
    (0,0,255), #blue
    (255,255,0), #yellow
    (0,255,255), #cyan
    (255,0,255), #magenta
    (192,192,192), #silver
    (128,128,128), #gray
    (128,0,0), #maroon
    (128,128,0), #olive
    (0,128,0), #green
    (128,0,128), #purple
    (0,128,128), #teal
    (0,0,128), #navy
    (255,165,0) #orange
)

def closest_color(rgb):
    r, g, b = rgb[0],rgb[1],rgb[2]
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def find_dominant_color(image):
    #Resizing parameters
    width, height = 150,150
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    #Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    return closest_color(dominant_color)




def run(path):
    #video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[10:]
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered"))[53:]
    failed = {}
    
    for videonr in tqdm(video_filelist):
        failed[videonr] = []
        #f = open(f"{path}/home/msb/{videonr}.tsv")
        f = open(f"{path}/msb/{videonr}.tsv")
        start_times = pd.read_csv(f, delimiter="\t")
        #for filename in tqdm(get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}")):
        for filename in tqdm(get_all_filesname(f"{path}/keyframes_filtered/{videonr}")):
            if filename != "Thumbs.db" and filename!= ".DAV":
                keyframe_id = get_keyframe_id(filename,videonr,path)
                keyframe_nr = int(keyframe_id)-1
                #image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
                #image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
                image = f"{path}/keyframes_filtered/{videonr}/{filename}"
                xPieces = 4
                yPieces = 3
                colors = []
                im = Image.open(image) 
                imgwidth, imgheight = im.size
                height = imgheight // yPieces
                width = imgwidth // xPieces
                for i in range(0, yPieces):
                    for j in range(0, xPieces):
                        box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                        a = im.crop(box)
                        color = find_dominant_color(a)
                        colors.append(color)

                color_list = list(sum(colors, ()))
                with CottontailDBClient('localhost', 1865) as client:
                    # Insert entry
                    entry = {
                        'video_id': Literal(stringData=str(videonr)),
                        'keyframe_id': Literal(intData=int(keyframe_id)), 
                        'dominant_color_vector': float_vector(color_list),
                        'start_time':Literal(intData = int(start_times.iloc[keyframe_nr]["startframe"]))
                    }
                    client.insert('tal_db', 'color_image', entry)

# change this path according to your computer
# path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"
#path = "/media/lkunam/Elements/Video Retrieval System"
path = 'Y:/TAL'

run(path)

"""
def processing(files,videonr,path):
    xPieces = 3
    yPieces = 4
    for filename in tqdm(files):
        keyframe_id = get_keyframe_id(filename,videonr,path)
        #image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
        image = f"{path}/keyframes_filtered_resized/{videonr}/{filename}"
        colors = []
        im = Image.open(image) 
        imgwidth, imgheight = im.size
        height = imgheight // yPieces
        width = imgwidth // xPieces
        for i in range(0, yPieces):
            for j in range(0, xPieces):
                box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                a = im.crop(box)
                color = find_dominant_color(a)
                colors.append(color)

        color_list = list(sum(colors, ()))
        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'video_id': Literal(stringData=str(videonr)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'dominant_color_vector': float_vector(color_list),
            }
            client.insert('tal_db', 'color_image', entry)





# change this path according to your computer
#path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"
path = "/media/lkunam/Elements/Video Retrieval System"


def run(path):
    nr_cores = 1
    #video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[:30]
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered_resized"))[:10]
    for videonr in video_filelist:
        #files = get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}")
        files = get_all_filesname(f"{path}/keyframes_filtered_resized/{videonr}")
        nr_processes = min(len(files), nr_cores)
        nr_processes = 2
        bins = np.array_split(files, nr_processes)

        jobs = []

        for i in range(nr_processes):
            #process_name = f"Process_{i}"
            jobs.append(Process(target=processing, args=(bins[i],videonr,path)))      

        for i, process in enumerate(jobs):
            process.start()
            print("started process_{}".format(i+1))

        for process in jobs:
            process.join()

run(path)
"""