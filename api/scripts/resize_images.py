import os
import glob
from PIL import Image

files = glob.glob('/home/kenichi/site/uploads/post/*')

width_base = 1000

for f in files:
    title, ext = os.path.splitext(f)
    if ext in ['.jpg', '.png']:
        file_size = os.path.getsize(f) /1024
        if file_size >500:
            img = Image.open(f)
            print(f)
            print(width_base/img.width)

            width_old = img.width
            height_old = img.height
            print("width:{0}".format(width_old))
            print("height:{0}".format(height_old))
        
            print("size:{0}".format(file_size))

            resized_width = 1000
            resized_height = height_old * (1000/width_old)
            print(resized_width)
            print(resized_height)

            img_resized = img.resize((int(resized_width), int(resized_height)), Image.LANCZOS)
            # new_file = os.path.join('/home/kenichi/site/uploads/', title + '_resized' + ext)
            img_resized.save(f)
            print(img_resized.size)

            print("----------------------")
        # img_resize = img.resize((int(img.width / 2), int(img.height / 2)))
        # img_resize.save(title + '_half' + ext)
