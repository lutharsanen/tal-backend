# import some common libraries
from PIL import Image
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector
import os
import multiprocessing
from multiprocessing import Process
import numpy as np


def find_dominant_color(filename):
    #Resizing parameters
    width, height = 150,150
    image = Image.open(filename)
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    #Get the most frequent color
    dominant_color1 = sorted_pixels[-1][1]
    dominant_color2 = sorted_pixels[-2][1]
    dominant_color3 = sorted_pixels[-3][1]
    print(dominant_color1)
    print(dominant_color2)
    print(dominant_color3)
    return (dominant_color1,dominant_color2,dominant_color3)


def processing(files,videonr,path, core_nr):
    for filename in files:
        keyframe_id = get_keyframe_id(filename,videonr,path)
        image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
        #store_color_sketch_from_masks(image, videonr, keyframe_id)
        im = Image.open(image) 
        im_quantized = im.quantize(25)
        im_quantized.save(f"quantized_color_{core_nr}.png")
        quantized_image = f"quantized_color_{core_nr}.png"
        Image.open(quantized_image)
        color = find_dominant_color(quantized_image)
        print(color)

        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'video_id': Literal(stringData=str(videonr)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'dominant_color_vector': float_vector(list(color)),
            }
            client.insert('tal_db', 'color_image', entry)
            os.remove(f"quantized_color_{core_nr}.png")




# change this path according to your computer
path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"

def run(path):
    nr_cores = 1
    video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[:30]
    for videonr in video_filelist:
        files = get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}")
        nr_processes = min(len(files), nr_cores)
        nr_processes = 1
        bins = np.array_split(files, nr_processes)

        jobs = []

        for i in range(nr_processes):
            #process_name = f"Process_{i}"
            jobs.append(Process(target=processing, args=(bins[i],videonr,path,i)))      

        for i, process in enumerate(jobs):
            process.start()
            print("started process_{}".format(i+1))

        for process in jobs:
            process.join()

run(path)