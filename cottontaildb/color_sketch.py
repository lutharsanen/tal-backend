import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger

# import some common libraries
import numpy as np
import os, cv2
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector
import json
from tqdm import tqdm

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from math import sqrt
from PIL import Image

COLORS = (
    (0,0,0),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (192,192,192),
    (128,128,128),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128)
)

def closest_color(rgb):
    r, g, b = rgb
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


def store_color_sketch_from_masks(image, video_id, keyframe_id):  
    detectron2_img = cv2.imread(image)
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(detectron2_img)

    #masks = outputs["instances"].pred_masks.cpu().numpy()
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    
    im = Image.open(image)
    for box in boxes:
        im_crop = im.crop(tuple(box))
        dominant_color = list(find_dominant_color(im_crop))
        
        ###### cottontail db logic ######
        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'video_id': Literal(stringData=str(video_id)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'sketch_vector': float_vector(box.tolist()),
                'color_vector': float_vector(dominant_color)}
            client.insert('tal_db', 'color_sketch', entry)
        # store rgb, border boxes, keyframe id and video id in database 



def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[:30]
    failed = {}
    for videonr in tqdm(video_filelist):
        failed[videonr] = []
        for filename in get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}"):
            keyframe_id = get_keyframe_id(filename,videonr,path)
            image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
            try:
                store_color_sketch_from_masks(image, videonr, keyframe_id)
            except:
                failed[videonr].append(filename)

       
    
    with open("failed_color_sketch.json", "w") as fi:
        fi.write(json.dumps(failed))
    

# change this path according to your computer
path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"


run(path)