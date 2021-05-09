import cottontail_pb2 as cottontail

# Schema

schema = cottontail.Schema(name="TAL")

def get_schema():
    return schema

# Video Metadata Feature

metadata_entity = cottontail.Entity(schema=schema, name="metadata_video")
columns = list()
columns.append(
    cottontail.ColumnDefinition(name="video_id", type=cottontail.Type.STRING, length=100, unique=False, nullable=False))
columns.append(
    cottontail.ColumnDefinition(name="data", type=cottontail.Type.STRING, length=100000, unique=False,
    nullable=False))

metadata_entity_definition = cottontail.EntityDefinition(entity=metadata_entity, columns=columns)

def get_metadata_entity():
    return metadata_entity

def get_metadata_entity_definition():
    return metadata_entity_definition

# Description Feature

description_entity = cottontail.Entity(schema=schema, name="feature_description")
columns = list()
columns.append(
    cottontail.ColumnDefinition(name="video_id", type=cottontail.Type.STRING, length=100, unique=False, nullable=False))
columns.append(
    cottontail.ColumnDefinition(name="keyframe_id", type=cottontail.Type.STRING, length=100, unique=False, 
    nullable=False))
columns.append(cottontail.ColumnDefinition(name="probability", type=cottontail.Type.DOUBLE, length=100, unique=False,
    nullable=False))

# to be continued
#columns.append()
