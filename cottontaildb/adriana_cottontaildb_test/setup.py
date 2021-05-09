import grpc
import cottontail_pb2_grpc as cottontail_rpc
import cottontail_pb2 as cottontail
import schema

def setup(channel):
    print('Create Database')
    ddl = cottontail_rpc.CottontailDDLStub(channel)

    # create schema
    ddl.CreateSchema(schema.get_schema())

    # create entities
    ddl.CreateEntity(schema.get_metadata_entity_definition())
   # ddl.CreateEntity(schema.get_description_entity_definition())
   # ddl.CreateEntity(schema.get_classification_entity_definition())
   # ddl.CreateEntity(schema.get_mask_entity_definition())

   