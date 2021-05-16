import torch
import detectron2

# import some common libraries
import numpy as np
import os, json, cv2, random
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, float_vector
from tqdm import tqdm

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

def store_classe_sketch_from_box(image, video_id, keyframe_id, counter):
    detectron2_img = cv2.imread(image)
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(detectron2_img)

    classes = outputs["instances"].pred_classes.cpu().numpy()
    boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    for data, box in zip(classes, boxes):
        box = box.tolist()
        num = data.item()
        counter +=1
        object = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes[num]
        ###### cottontail db logic ######
        # store object, border boxes, keyframe id and video id in database
        with CottontailDBClient('localhost', 1865) as client:
        # Insert entry
            entry = {
                'object_id':Literal(intData = counter),
                'video_id': Literal(stringData=str(video_id)),
                'keyframe_id': Literal(intData=int(keyframe_id)), 
                'sketch_vector': float_vector(box),
                'object': Literal(stringData = object)}
            client.insert('tal_db', 'object_sketch', entry)
    
    return counter


def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/keyframes_filtered_resized"))[:100]
    failed = {}
    counter = 0
    for videonr in tqdm(video_filelist):
        failed[videonr] = []
        for filename in get_all_filesname(f"{path}/keyframes_filtered_resized/{videonr}"):
            if filename != "Thumbs.db":
                keyframe_id = int(get_keyframe_id(filename,videonr,path))
                image = f"{path}/keyframes_filtered_resized/{videonr}/{filename}"
                #try:
                new_counter = store_classe_sketch_from_box(image, videonr, keyframe_id, counter)
                counter = new_counter
                #except:
                #failed[videonr].append(filename)
        
    with open("failed_object_sketch.json", "w") as fi:
        fi.write(json.dumps(failed))



# change this path according to your computer
path = "/media/lkunam/Elements/Video Retrieval System"

run(path)