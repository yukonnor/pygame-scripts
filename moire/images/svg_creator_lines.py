'''
Creates an SVG image of a different width lines.
- Pattern 1: Small to large lines

'''

import svgwrite as svg


file_path = '/Users/concon/Desktop/' # save to desktop
filename = 'lines_1'

line_count = 40
svg_size = 1000
max_line_width = svg_size / line_count

# Create File
mysvg = svg.Drawing(file_path + filename + '.svg', (svg_size, svg_size), fill='none', viewBox=(f'0 0 {svg_size} {svg_size}'), profile='full')  # filenamme, size(x,y), kwargs
print(mysvg.tostring())

# Create a group in the SVG for the paths (groups can be rotated, masked, etc)
group = mysvg.add(mysvg.g())

# Draw Lines 

# Expanding width lines
for i in range(line_count):
    line_width_incrememt = max_line_width / line_count
    group.add(mysvg.line((0, i * max_line_width), (svg_size, i * max_line_width), stroke='black',  stroke_width=i * line_width_incrememt))  
    


# Save file to filename set when image defined
mysvg.save(True)

print(mysvg.tostring())