from img2vec_pytorch import Img2Vec
from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('test_schema')
    # Define entity feature vector columns
    feature_vector_columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('feature_vector', Type.FLOAT_VEC, nullable=True, length=3)
    ]
    # Create entity feature vector
    client.create_entity('test_schema', 'test_feature_vector', feature_vector_columns)

    img2vec = Img2Vec()

    
    # Read in an image
    img = Image.open("test.jpg")
    # Get a vector from img2vec, returned as a torch FloatTensor
    test_vector = img2vec.get_vec(img)

    details = client.get_entity_details('test_schema', 'test_feature_vector')
    print(details)

    # Insert entry
    entry = {'keyframe_id': Literal(intData=2), 'feature_vector': float_vector([1.2,1.3,1.7])}
    client.insert('test_schema', 'test_feature_vector', entry)