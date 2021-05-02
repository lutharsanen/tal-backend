from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np
# Some basic setup:
# Setup detectron2 logger
#import detectron2
from detectron2.utils.logger import setup_logger
import cv2