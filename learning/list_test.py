
polygons = []
active_polygon = 0
active_point = 0

NUM_POLYGONS = 7

for i in range(NUM_POLYGONS):
    polygons.append([[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]])


print(polygons)


for i in range(50):

    polygons[active_polygon][active_point][1] += 2

    if active_polygon == (NUM_POLYGONS - 1):
        active_polygon = 0
    else:
        active_polygon += 1


    if active_point == 5:
        active_point = 0
    else:
        active_point += 1


    
    print('\n')
    print(active_polygon)
    print(active_point)
    print(polygons)