from cottontaildb_client import CottontailDBClient, Type, column_def
from PIL import Image
import numpy as np

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('tal_db')
   
    # Define entity color_sketch columns
    color_sketch_columns = [
        column_def('video_id', Type.INTEGER, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('sketch_vector', Type.FLOAT_VEC, nullable=True, length=4),
        column_def('color_vector', Type.INT_VEC, nullable=True, length=3)
    ]
    # Create entity color sketch
    client.create_entity('tal_db', 'color_sketch', color_sketch_columns)

    # Define entity color_sketch columns
    object_sketch_columns = [
        column_def('video_id', Type.INTEGER, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('sketch_vector', Type.FLOAT_VEC, nullable=True, length=4),
        column_def('object', Type.STRING, nullable=False)
    ]
    # Create entity color sketch
    client.create_entity('tal_db', 'object_sketch', object_sketch_columns)

    # Define entity color_sketch columns
    color_image_columns = [
        column_def('video_id', Type.INTEGER, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('dominant_color_two', Type.INT_VEC, nullable=True, length=3),
        column_def('dominant_color_one', Type.INT_VEC, nullable=True, length=3),
        column_def('dominant_color_three', Type.INT_VEC, nullable=True, length=3)
    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'color_image', color_image_columns)


    # Read in an image
    
    # Get a vector from img2vec, returned as a torch FloatTensor
    #test_vector = img2vec.get_vec(img)

    #details = client.get_entity_details('test_schema', 'test_feature_vector')
    #print(details)