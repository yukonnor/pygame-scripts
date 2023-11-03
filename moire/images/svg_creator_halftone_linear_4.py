'''
Creates an SVG image of a dot matrix.
- Max laptop full screen res: 1440, 900 

'''

import svgwrite as svg


file_path = '/Users/concon/Desktop/' # save to desktop
filename = 'halftone_linear_4'

col_count = 40
row_count = col_count
svg_size = 1000
tile_size = svg_size / col_count

start_radius = 5
end_radius = 16
px_step_size = round((end_radius - start_radius) / (col_count/2),1)

# Create File
mysvg = svg.Drawing(file_path + filename + '.svg', (svg_size, svg_size), fill='none', viewBox=(f'0 0 {svg_size} {svg_size}'), profile='full')  # filenamme, size(x,y), kwargs
print(mysvg.tostring())

# Create a group in the SVG for the paths (groups can be rotated, masked, etc)
group = mysvg.add(mysvg.g())

# Draw halftone dots 
        
# descending (Dark to Light)
for col in range(col_count):
    for row in range(int(row_count / 2)):
        center_x = (col * tile_size) + tile_size / 2
        center_y = (row * tile_size) + tile_size / 2
        radius =  round(end_radius - (px_step_size * (row + 1)), 2)
        group.add(mysvg.circle((center_x, center_y), radius, fill='black'))   # (center_x, center_y), radius, fill color
        
# ascending (From midway: Light to Dark)
for col in range(col_count):
    for row in range(int(row_count / 2)):
        center_x = (col * tile_size) + tile_size / 2
        center_y = (row * tile_size) + tile_size / 2 + (tile_size * (row_count / 2))
        radius =  round(start_radius + (px_step_size * (row + 1)), 2)
        group.add(mysvg.circle((center_x, center_y), radius, fill='black'))   # (center_x, center_y), radius, fill color

# Save file to filename set when image defined
mysvg.save(True)

print(mysvg.tostring())