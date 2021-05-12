from cottontaildb_client import CottontailDBClient
from google.protobuf.json_format import MessageToDict


with CottontailDBClient('localhost', 1865) as client:
    
    #result = client.knn([1.3,1.3,4.7,2.4],"tal_db","color_sketch","sketch_vector", ["video_id", "keyframe_id", "distance"])
    #for i in result:
    #    test = MessageToDict(i)
    #    p = test["tuples"]
    #    for pi in p:
    #        print(pi["data"])
    
    #result = client.select("tal_db","object_sketch",["video_id", "keyframe_id"])
    #print(list(result))
    #print("hello")
    print(client.get_entity_details("tal_db", "color_sketch"))
    print(client.get_entity_details("tal_db", "color_image"))
    print(client.get_entity_details("tal_db", "object_sketch"))
    ########################################################