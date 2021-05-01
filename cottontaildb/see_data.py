from img2vec_pytorch import Img2Vec
from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np

with CottontailDBClient('localhost', 1865) as client:
    details = client.list_entities('test_schema')
    print(details)


    img2vec = Img2Vec()

    
    # Read in an image
    #img = Image.open("test.jpg")
    img = Image.open("../../tal-feature-engineering/shot00032_13_RKF.png")
    # Get a vector from img2vec, returned as a torch FloatTensor
    image_array = img2vec.get_vec(img)

    print((image_array))
    