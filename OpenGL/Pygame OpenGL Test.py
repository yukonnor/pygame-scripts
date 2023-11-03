import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# CUBE has
# 8 verticies (aka nodes)
# 12 lines connecting the verticies
# 6 faces

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

def Cube():
    glBegin(GL_LINES)  # input const telling GL what type of drawing we're making
    
    for edge in edges:
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