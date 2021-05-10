from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np
# Some basic setup:
# Setup detectron2 logger
#import detectron2
from detectron2.utils.logger import setup_logger
import cv2

with CottontailDBClient('localhost', 1865) as client:
    result = client.select("tal_db","color_sketch")
    print(list(result))