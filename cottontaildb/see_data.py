#import torch, torchvision
from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np
# Some basic setup:
# Setup detectron2 logger
#import detectron2
from detectron2.utils.logger import setup_logger
import cv2

im = cv2.imread("./shot00032_13_RKF.png")

# import some common libraries
import numpy as np
import os, json, cv2, random
import matplotlib.pyplot as plt

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

#with CottontailDBClient('localhost', 1865) as client:
    #details = client.list_entities('test_schema')
    #print(details)


im = cv2.imread("test.jpg")
cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)
outputs = predictor(im)
box_vector = outputs["instances"].pred_boxes.tensor.cpu().numpy()
classes_vector = outputs["instances"].pred_classes.tensor.cpu().numpy()

for b, c in zip(box_vector, classes_vector):
    print(b, c)

    #for vector in box_vector:
    #    vector_float = vector.astype(float)
    #    print(type(vector_float[0]))


    # Read in an image
    #img = Image.open("test.jpg")
    #img = Image.open("../../tal-feature-engineering/shot00032_13_RKF.png")
    # Get a vector from img2vec, returned as a torch FloatTensor

     # Insert entry
    #entry = {'keyframe_id': Literal(intData=2), 'feature_vector': float_vector(box_vector_float)}
    #client.insert('test_schema', 'test_feature_vector', entry)
