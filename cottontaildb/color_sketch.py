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
    print(dominant_color)
    return closest_color(dominant_color)


def store_color_sketch_from_masks(image, video_id, keyframe_id, counter):  
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
        counter +=1
        ###### cottontail db logic ######
        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'color_id': Literal(intData = counter),
                'video_id': Literal(stringData=str(video_id)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'sketch_vector': float_vector(box.tolist()),
                'color_vector': float_vector(dominant_color)}
            client.insert('tal_db', 'color_sketch', entry)
    return counter

        # store rgb, border boxes, keyframe id and video id in database 



def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered_resized"))[:100]
    failed = {}
    counter = 0
    for videonr in tqdm(video_filelist):
        failed[videonr] = []
        for filename in get_all_filesname(f"{path}/keyframes_filtered_resized/{videonr}"):
            if filename != "Thumbs.db":
                keyframe_id = get_keyframe_id(filename,videonr,path)
                image = f"{path}/keyframes_filtered_resized/{videonr}/{filename}"
                #try:
                new_counter = store_color_sketch_from_masks(image, videonr, keyframe_id,counter)
                counter = new_counter
                #except:
                    #failed[videonr].append(filename)

       
    
    #with open("failed_color_sketch.json", "w") as fi:
        #fi.write(json.dumps(failed))
    

# change this path according to your computer
path = "/media/lkunam/Elements/Video Retrieval System"


run(path)