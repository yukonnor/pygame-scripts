'''
Creates an SVG image of a radiating triangles:
- 40 trianges (one every 9 degrees)
  - shared origin point
  - every

First Seciont (5 triangles)
First triange:
(0,0) --> (XMAX, 0) --> (XMAX, 0 + Height)
Second:
(0,0) --> (XMAX, Height * 2) --> (XMAX, Height * 3)
Nth:

'''

import svgwrite as svg


file_path = '/Users/concon/Desktop/' # save to desktop
filename = 'radial_1'

poly_count = 40
svg_size = 1000
center = [svg_size/2, svg_size/2]
tri_height = svg_size / (poly_count / 4) 

# Create File
mysvg = svg.Drawing(file_path + filename + '.svg', (svg_size, svg_size), fill='none', viewBox=(f'0 0 {svg_size} {svg_size}'), profile='full')  # filenamme, size(x,y), kwargs
print(mysvg.tostring())

# Create a group in the SVG for the paths (groups can be rotated, masked, etc)
group = mysvg.add(mysvg.g())

# Draw polygons 
range = range(-5, 5)

# Right side
for i in range:
    point_1 = (center[0], center[1])
    point_2 = (svg_size, center[1] + (i * tri_height))
    point_3 = (svg_size, center[1] + (i * tri_height) + tri_height/2)
    group.add(mysvg.polygon([point_1, point_2, point_3], fill='black'))  
    
# Bottom side
for i in range:
    point_1 = (center[0], center[1])
    point_2 = (center[0] + (i * tri_height) + tri_height/2, svg_size)
    point_3 = (center[0] + ((i+1) * tri_height), svg_size)
    group.add(mysvg.polygon([point_1, point_2, point_3], fill='black'))  
    
# Left side 
for i in range:
    point_1 = (center[0], center[1])
    point_2 = (0, center[1] + (i * tri_height) + tri_height/2)
    point_3 = (0, center[1] + ((i+1) * tri_height))
    group.add(mysvg.polygon([point_1, point_2, point_3], fill='black'))  
    
# Top side
for i in range:
    point_1 = (center[0], center[1])
    point_2 = (center[0] + (i * tri_height), 0)
    point_3 = (center[0] + (i * tri_height) + tri_height/2, 0)
    group.add(mysvg.polygon([point_1, point_2, point_3], fill='black'))  

# Save file to filename set when image defined
mysvg.save(True)

print(mysvg.tostring())