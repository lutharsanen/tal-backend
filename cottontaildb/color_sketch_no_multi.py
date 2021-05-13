import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger

# import some common libraries
import numpy as np
import os, cv2
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector, int_vector
import json
import multiprocessing
from multiprocessing import Process

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

import math
from PIL import Image


def find_dominant_color(filename):
    #Resizing parameters
    width, height = 150,150
    image = Image.open(filename)
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    print(sorted_pixels)
    #Get the most frequent color
    dominant_color = sorted_pixels[-1][1]
    #print(dominant_color)
    return dominant_color


def store_color_sketch(image, video_id, keyframe_id):
    im = Image.open(image) 
    im_quantized = im.quantize(256)
    im_quantized.save("quantized.png")
    Image.open("quantized.png") 
    detectron2_img = cv2.imread("quantized.png")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(detectron2_img)

    #masks = outputs["instances"].pred_masks.cpu().numpy()
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    
    for box in boxes:
        im_crop = im_quantized.crop(tuple(box))
        im_crop.save('temporary_image.png', quality=95)
        dominant_color = list(find_dominant_color("temporary_image.png"))
        
        ###### cottontail db logic ######
        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'video_id': Literal(stringData=str(video_id)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'sketch_vector': float_vector(box.tolist()),
                'color_vector': int_vector(dominant_color)}
            client.insert('tal_db', 'color_sketch', entry)
        # store rgb, border boxes, keyframe id and video id in database 



def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[:30]
    failed = {}
    for videonr in video_filelist:
        failed[videonr] = []
        for filename in get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}"):
            keyframe_id = get_keyframe_id(filename,videonr,path)
            image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
            try:
                store_color_sketch(image, videonr, keyframe_id)
            except:
                failed[videonr].append(filename)
            break
        break

       
    
    with open("failed_object_sketch.json", "w") as fi:
        fi.write(json.dumps(failed))
    

# change this path according to your computer
path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"


run(path)