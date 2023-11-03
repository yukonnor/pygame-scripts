'''
Creates an SVG image of a dot matrix based on an input image
'''

import svgwrite as svg
from PIL import Image

# Input img file
img = Image.open('/Users/concon/pygame-scripts/moire/images/Rings_2.png')
pixel_count = 32 # number of pixels (and thus dots) wide

# Final output SVG file
file_path = '/Users/concon/Desktop/' # save to desktop
filename = f'dot_rings_{pixel_count}'


def pixelate(image, final_res = 16):
    
    # Resize smoothly down to 16x16 pixels
    imgSmall = image.resize((final_res,final_res), resample=Image.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(image.size, Image.NEAREST)
    
    return imgSmall, result # imgSmall is the scaled down image, result is the pixelated image scaled back to original img size


# Pixelate Image and Get Pixel Vaules
pixelated_img_small, pixelated_img_full = pixelate(img, pixel_count)
img_small = pixelated_img_small.load() # get the pixel values from the small image
pixelated_img_full.save(file_path + filename + '.png')

# Create SVG File
col_count = pixel_count
row_count = pixel_count
svg_size = 1000
tile_size = round(svg_size / col_count,2)


max_dot_radius = tile_size / 1.5 # max dot size (black) corresponds with darkest pixels
min_dot_radius = 5               # min dot size corresponds with brightest pixels
min_brightness = 0
max_brightness = 255

# Create svg
mysvg = svg.Drawing(file_path + filename + '.svg', (svg_size, svg_size), fill='none', viewBox=(f'0 0 {svg_size} {svg_size}'), profile='full')  # filenamme, size(x,y), kwargs

# Create a group in the SVG for the paths (groups can be rotated, masked, etc)
group = mysvg.add(mysvg.g())

# Draw dots 
for row in range(row_count):
    for col in range(col_count):
        center_x = (col * tile_size) + tile_size / 2
        center_y = (row * tile_size) + tile_size / 2
        
        # get the 'red' value of the pixel to determine its brightness (r,g,b will be equal as we're using B&W images)
        brightness = img_small[row,col][0]
        
        # Map min_color to min_dot_size and max_color to max_dot_size
        mapped_brightness = (((brightness - min_brightness) * (min_dot_radius - max_dot_radius)) / (max_brightness - min_brightness)) + max_dot_radius
        radius =  round(mapped_brightness) 
        
        group.add(mysvg.circle((center_x, center_y), radius, fill='black'))   # (center_x, center_y), radius, fill color

# Save file to filename set when image defined
mysvg.save(True)

print(mysvg.tostring())