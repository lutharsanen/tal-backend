from sketch import run as object_sketch_run
from color_image import run as color_image_run

path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"

object_sketch_run(path)
print("object_sketch done")
color_image_run(path)
print("color_image done")

