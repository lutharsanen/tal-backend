import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger

# import some common libraries
import numpy as np
import os, cv2
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector, int_vector
import json

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
    #Get the most frequent color
    dominant_color = sorted_pixels[-2][1]
    return dominant_color

def get_mask_image(mask, box,image):
    mask_h = int(math.ceil(box[3] - box[1]))
    mask_w = int(math.ceil(box[2] - box[0]))

    original_img = np.array(Image.fromarray(image))

    temp_mask = np.zeros((mask_h, mask_w))

    for h_idx in range(int(box[1]), int(box[3])):
        for w_idx in range(int(box[0]), int(box[2])):
            temp_mask[h_idx - int(box[1])][w_idx - int(box[0])] = mask[h_idx][w_idx]

    temp_masks_ints = temp_mask.astype(int)

    temp_mask_fill = np.zeros((mask_h, mask_w, 4))
    for h_idx, h_bw in enumerate(temp_masks_ints):
        for w_idx, w_bw in enumerate(h_bw):
            if (w_bw == 0):
                temp_mask_fill[h_idx][w_idx] = [83,62,65,0.2]
            else:
                orig_w = int(math.ceil(w_idx + box[0]))
                orig_h = int(math.ceil(h_idx + box[1]))
                temp_mask_fill[h_idx][w_idx] = np.append(original_img[orig_h][orig_w],1)

    return temp_mask_fill

def store_color_sketch_from_masks(image, video_id, keyframe_id):
    im = Image.open(image) 
    im_quantized = im.quantize(25)
    im_quantized.save("quantized.png")
    detectron2_img = cv2.imread("quantized.png")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(detectron2_img)

    masks = outputs["instances"].pred_masks.cpu().numpy()
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    
    for index, mask in enumerate(masks):
        temp_mask_fill = get_mask_image(mask, boxes[index], detectron2_img)
        cv2.imwrite("temporary_image.png",temp_mask_fill[:,:,0:3])
        Image.open("temporary_image.png")
        dominant_color = list(find_dominant_color("temporary_image.png"))
        box = boxes[index].tolist()
        ###### cottontail db logic ######
        with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
            entry = {
                'video_id': Literal(intData=int(video_id)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'sketch_vector': float_vector(box),
                'color_vector': int_vector(dominant_color)}
            print(entry)
            client.insert('tal_db', 'color_sketch', entry)
        # store rgb, border boxes, keyframe id and video id in database 
        os.remove("temporary_image.png")
        os.remove("quantized.png")


# change this path according to your computer
path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"

def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))[:2]
    failed = {}
    for videonr in video_filelist:
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

run(path)