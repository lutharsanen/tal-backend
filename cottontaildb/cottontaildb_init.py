from cottontaildb_client import CottontailDBClient, Type, column_def
from PIL import Image
import numpy as np

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('tal_db')
   
    # Define entity sketch columns
    sketch_columns = [
        column_def('box_id', Type.INTEGER, nullable=False),
        column_def('video_id', Type.STRING, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('sketch_vector', Type.FLOAT_VEC, nullable=True, length=4),
        column_def('color_vector', Type.FLOAT_VEC, nullable=True, length=3),
        column_def('object', Type.STRING, nullable=False),
        column_def('start_time', Type.INTEGER, nullable=False)
    ]
    # Create entity color sketch
    client.create_entity('tal_db', 'sketch', sketch_columns)


    # Define entity color_image columns
    color_image_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('dominant_color_vector', Type.FLOAT_VEC, nullable=True, length=36),
        column_def('start_time', Type.INTEGER, nullable=False)

    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'color_image', color_image_columns)


    # Define entity text columns
    text_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('tesseract_text', Type.STRING, nullable=True),
        column_def('start_time', Type.INTEGER, nullable=False),
        column_def('image_capture_text', Type.STRING, nullable=True)
    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'text_search', text_columns)

    # Define entity tag columns
    tag_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('tags', Type.STRING, nullable=False)
    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'video_tags', tag_columns)

    # Define entity video columns
    video_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('title', Type.STRING, nullable=False),
        column_def('description', Type.STRING, nullable=False)
    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'video_search', video_columns)

    # Define entity video columns
    audio_columns = [
        column_def('video_id', Type.STRING, nullable=False),
        column_def('audio_transcription', Type.STRING, nullable=False)
    ]
    # Create entity feature vector
    client.create_entity('tal_db', 'transcription', audio_columns)


