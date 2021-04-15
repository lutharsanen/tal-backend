from cottontaildb_client import CottontailDBClient, Type, Literal, column_def

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('example_schema')
    # Define entity columns
    columns = [
        column_def('id', Type.STRING, nullable=False),
        column_def('value', Type.INTEGER, nullable=True)
    ]
    # Create entity
    client.create_entity('example_schema', 'example_entity', columns)
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
