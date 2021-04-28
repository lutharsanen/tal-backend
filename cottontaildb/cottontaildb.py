from cottontaildb_client import CottontailDBClient, Type, Literal, column_def

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('feature-extraction-db')
    # Define entity columns
    columns = [
        column_def('keyframe_id', Type.INTEGER, nullable=False),
        column_def('feature_vector', Type.INTEGER, nullable=True),
        column_def('video_id', Type.INTEGER, nullable=False),
        column_def('start_time', Type.INTEGER, nullable=False),
        column_def('end_time', Type.INTEGER, nullable=False),

    ]
    # Create entity
    client.create_entity('tal_schema', 'tal_entity', columns)
    # Insert entry
    entry = {'id': Literal(stringData='test_1'), 'value': Literal(intData=1)}
    client.insert('example_schema', 'example_entity', entry)
    # Insert batch
    """
    batch = [
        ('example_schema', 'example_entity', {'id': Literal(
            stringData='test_10'), 'value': Literal(intData=10)}),
        ('example_schema', 'example_entity', {'id': Literal(
            stringData='test_20'), 'value': Literal(intData=20)})
    ]
    client.insert_batch(batch)
"""