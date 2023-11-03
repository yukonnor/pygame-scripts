import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# CUBE has
# 8 vertices (aka nodes)
# 12 lines connecting the vertices
# 6 faces
# Cube surfaces have 4 vertices each

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)  
    )

# edges aka lines, connections between vertices
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

# Colors in OpenGL  0 min, 1 max
colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,1,1),
    (0,1,1)
)

def set_vertices(max_distance):
    x_value_change = random.randrange(-10,10)
    y_value_change = random.randrange(-10,10)
    z_value_change = random.randrange(-1 * max_distance, -40) 
    
    new_vertices = []
    
    for vert in vertices:
        new_vert = []
        
        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change
        
        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)
        
        new_vertices.append(new_vert)
    
    return new_vertices

def Cube(vertices):
         
    glBegin(GL_QUADS) # tell GL that we're drawing quadrangles
    for surface in surfaces:
        x = 0
        for vertex in surface:
            glColor3fv(colors[x])  # Colors vertices. GL then smooths out color between vertices.
            x+=1
            glVertex3fv(vertices[vertex])
    glEnd()
    
    glBegin(GL_LINES)  # input const telling GL what type of drawing we're making
    for edge in edges:
        glColor3fv((1,0,0))  # Colors edges. 0 min, 1 max
        for vertex in edge:
            glVertex3fv(vertices[vertex]) # Goolge "glVertex3fv"
    glEnd()
    
    
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  # prepares display for some openGL
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 250.0)  # sets field of view (degrees), aspect ratio, znear and zfar for 'clipping planes'
    glTranslatef(random.randrange(-3,3), random.randrange(-3,3), -40)     # x,y,z params for object's position (or camera's?)
    #glRotatef(0, 0, 0, 0)          # rotates the object n degrees around the x,y,z axis
    
    object_passed = False
    
    x_vel = 0
    y_vel = 0
    
    max_distance = 300 # max distance away we'll draw a cube
    
    cube_dict = {}
    
    for i in range(65):
        cube_dict[i] = set_vertices(max_distance)
        
    
    while True:        # run the game while the object is still in front of the camera
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # checking pressed keys for held down keys            
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_LEFT]:
            glTranslatef(.3, 0, 0) 
        if keys[pygame.K_RIGHT]:
            glTranslatef(-.3, 0, 0) 
        if keys[pygame.K_UP]:
            glTranslatef(0, -.3, 0) 
        if keys[pygame.K_DOWN]:
            glTranslatef(0, .3, 0) 
                        
        # Get where the camera is currently
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print(x)   
        '''
           [[ 1.81066024  0.          0.          0.        ]
            [ 0.          2.41421366  0.          0.        ]
            [ 0.          0.         -1.00400805 -1.        ]
            [ 0.          0.          9.83968067 10.        ]]
          AS we know we started the camera at (0.0, 0.0, -10) we can see that z is in fourth list [x, y, z_new, z_old]
          When x_new is past cube (-1, ie cube went past camera) we can draw new cube
        '''
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        
        if camera_z < -1:
            pass
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # clears frame of gl object (comment out to draw trails)
        
        # Move cubes towards camera
        glTranslatef(0, 0, 0.50) 
        
        # Draw cubes
        for i in cube_dict:
            Cube(cube_dict[i])
        
        pygame.display.flip()
        pygame.time.wait(10)
 

main()
    
pygame.quit()
quit()