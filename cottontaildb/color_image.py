# import some common libraries
from PIL import Image
from cottontail_helper import get_all_filesname, get_keyframe_id
from cottontaildb_client import CottontailDBClient, Literal, int_vector



def find_dominant_color(filename):
    im = Image.open(filename) 
    im_quantized = im.quantize(25)
    im_quantized.save("quantized.png")
    #Resizing parameters
    width, height = 150,150
    image = Image.open("quantized.png")
    image = image.resize((width, height),resample = 0)
    #Get colors from image object
    pixels = image.getcolors(width * height)
    #Sort them by count number(first element of tuple)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    print(sorted_pixels)
    #Get the most frequent color
    dominant_color1 = sorted_pixels[-1][1]
    dominant_color2 = sorted_pixels[-2][1]
    dominant_color3 = sorted_pixels[-3][1]
    return (dominant_color1 ,dominant_color2 ,dominant_color3)

# change this path according to your computer
path = "/run/user/1000/gvfs/dav:host=tal.diskstation.me,port=5006,ssl=true"

def run(path):
    video_filelist = sorted(get_all_filesname(f"{path}/home/keyframes_filtered"))
    for videonr in video_filelist:
        for filename in get_all_filesname(f"{path}/home/keyframes_filtered/{videonr}"):
            keyframe_id = videonr,get_keyframe_id(filename,videonr,path)
            image = f"{path}/home/keyframes_filtered/{videonr}/{filename}"
            #store_color_sketch_from_masks(image, videonr, keyframe_id)
            color = find_dominant_color(image)

            with CottontailDBClient('localhost', 1865) as client:
            # Insert entry
                entry = {
                    'video_id': Literal(intData=int(videonr)),
                    'keyframe_id': Literal(intData=int(keyframe_id)), 
                    'dominant_color_one': int_vector(list(color[0])),
                    'dominant_color_two': int_vector(list(color[1])),
                    'dominant_color_three': int_vector(list(color[2]))
                }
                print(entry)
                client.insert('tal_db', 'color_image', entry)
