import svgwrite as svg


file_path = '/Users/concon/Desktop/' # save to desktop
filename = 'my_svg'

canvas_size = 500
shape_width = 100

# Create File
mysvg = svg.Drawing(file_path + filename + '.svg', (canvas_size, canvas_size), viewBox=(f'0 0 {canvas_size} {canvas_size}'), fill='none', profile='full')  # filenamme, size(x,y), kwargs

# Create a group for elements
group = mysvg.add(mysvg.g())

# Add shapes to group
group.add(mysvg.rect((0, 0), (shape_width, shape_width), fill='blue'))
group.add(mysvg.rect((0, canvas_size - shape_width), (shape_width, shape_width), fill='green'))  
group.add(mysvg.rect((canvas_size - shape_width, 0), (shape_width, shape_width), fill='red'))  
group.add(mysvg.rect((canvas_size - shape_width, canvas_size - shape_width), (shape_width, shape_width), fill='yellow'))

group.add(mysvg.line((shape_width, 5), (canvas_size - shape_width, 5), stroke='black', stroke_width='10'))
group.add(mysvg.line((canvas_size - 5, shape_width), (canvas_size - 5, canvas_size - shape_width), stroke='black', stroke_width='10'))
group.add(mysvg.line((canvas_size - shape_width, canvas_size - 5), (shape_width, canvas_size - 5), stroke='black', stroke_width='10'))
group.add(mysvg.line((5, shape_width), (5, canvas_size - shape_width), stroke='black', stroke_width='10'))
group.add(mysvg.line((shape_width, shape_width), (canvas_size - shape_width, canvas_size - shape_width), stroke='black', stroke_width='2'))
group.add(mysvg.line((canvas_size - shape_width, shape_width), (shape_width, canvas_size - shape_width), stroke='black', stroke_width='2'))


group.add(mysvg.circle((canvas_size/2, canvas_size/2), 20, fill='red'))
group.add(mysvg.circle((canvas_size/2, canvas_size/2), 3, fill='black'))

# Save file to filename set when image defined
mysvg.save(True)

print(mysvg.tostring())