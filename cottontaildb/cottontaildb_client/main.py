import grpc
import cottontail_pb2_grpc as cottontail_rpc
import cottontail_pb2 as cottontail
import reset
import setup
# import import_description_feature
# import import_classification_feature
# import import_mask_feature
# import import_video_metadata

channel = grpc.insecure_channel('localhost:1865')

reset.reset(channel)
# setup.setup(channel)

# import_description_feature.do(channel)
# import_classification_feature.do(channel)
# import_mask_feature.do(channel)
# import_video_metadata.do(channel)

