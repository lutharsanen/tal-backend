from cottontaildb_client import CottontailDBClient, Type, Literal, column_def

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('example_schema')
    # Define entity feature vector columns
    feature_vector_columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('feature_vector', Type.INTEGER, nullable=True),
        column_def('video_id', Type.INTEGER, nullable=False)
    ]
    # Create entity feature vector
    client.create_entity('tal_schema', 'tal_feature_vector', feature_vector_columns)

    # Define entity color columns
    color_columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('feature_vector', Type.INTEGER, nullable=True),
        column_def('video_id', Type.INTEGER, nullable=False)
    ]

    # Create entity color
    client.create_entity('tal_schema', 'tal_color',color_columns)
    
    # Define entity object detection columns
    feature_vector_columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('objects', Type.INTEGER, nullable=True),
        column_def('video_id', Type.INTEGER, nullable=False)
    ]


    """
    # Insert entry
    entry = {'id': Literal(stringData='test_1'), 'value': Literal(intData=1)}
    client.insert('example_schema', 'example_entity', entry)
    # Insert batch
    batch = [
        ('example_schema', 'example_entity', {'id': Literal(
            stringData='test_10'), 'value': Literal(intData=10)}),
        ('example_schema', 'example_entity', {'id': Literal(
            stringData='test_20'), 'value': Literal(intData=20)})
    ]
    client.insert_batch(batch)
    """