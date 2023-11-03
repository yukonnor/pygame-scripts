#import those 2 modules I mentioned
from PIL import Image
import numpy as np

img = Image.open('/Users/concon/pygame-scripts/moire/images/Rings.png')

def pixelate_v1(image, pixelation_amount):
    
    #new dimensions via list comprehension
    new_dims = [int(np.round(a*pixelation_amount)) for a in image.size]
    
    #downsample, upsample, and return
    return image.resize(new_dims).resize(image.size, resample = 4)

def pixelate_v2(image, final_res = 16):
    
    # Resize smoothly down to 16x16 pixels
    imgSmall = image.resize((final_res,final_res), resample=Image.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(image.size, Image.NEAREST)
    
    return result


# pixelate the image (.10 = pretty pixely, lower values are lower resolution)
#pixaleted_img = pixelate_v1(img, .02)

# input the amount of pixels you want
pixaleted_img = pixelate_v2(img, 16)

#save the image
pixaleted_img.save('/Users/concon/pygame-scripts/moire/images/pixelated_1.png')