import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# CUBE has
# 8 verticies (aka nodes)
# 12 lines connecting the verticies
# 6 faces
# Cube surfaces have 4 verticies each

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)  
    )

# edges aka lines, connections between verticies
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

def Cube():
         
    glBegin(GL_QUADS) # tell GL that we're drawing quadrangles
    for surface in surfaces:
        x = 0
        for vertex in surface:
            glColor3fv(colors[x])  # Colors VERTICIES. GL then smooths out color between verticies.
            x+=1
            glVertex3fv(verticies[vertex])
    glEnd()
    
    glBegin(GL_LINES)  # input const telling GL what type of drawing we're making
    for edge in edges:
        glColor3fv((1,0,0))  # Colors edges. 0 min, 1 max
        for vertex in edge:
            glVertex3fv(verticies[vertex]) # Goolge "glVertex3fv"
    glEnd()
    
    
def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)  # prepares display for some openGL
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)  # sets field of view (degrees), aspect ratio, znear and zfar for 'clipping planes'
    glTranslatef(0.0, 0.0, -5)     # x,y,z params for object (move object) 
    glRotatef(0, 0, 0, 0)          # rotates object n degrees arouce x,y,z axis
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        glRotatef(1, 3, 2, 1) # set object to rotate one degree every frame      
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # clears frame of gl object (comment out to draw trails)
        
        Cube()
        
        pygame.display.flip()
        pygame.time.wait(10)
        
main()