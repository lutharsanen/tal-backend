from cottontaildb_client import CottontailDBClient, Type, Literal, column_def, float_vector
from PIL import Image
import numpy as np

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('test_schema')
    # Define entity feature vector columns
    feature_vector_columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('feature_vector', Type.BLOB, nullable=True)
    ]
    # Create entity feature vector
    client.create_entity('test_schema', 'test_feature_vector', feature_vector_columns)

    
    # Read in an image
    # Get a vector from img2vec, returned as a torch FloatTensor
    #test_vector = img2vec.get_vec(img)

    details = client.get_entity_details('test_schema', 'test_feature_vector')
    print(details)

    # Insert entry
    entry = {'keyframe_id': Literal(intData=2), 'feature_vector': float_vector((0.3,0.4,0.7,0.9))}
    client.insert('test_schema', 'test_feature_vector', entry)
