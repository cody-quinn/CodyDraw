import math
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders

def point_exists(point_list, x, y):
    exists = False # Variable to keep track of if the point exists or not
    # Checking to make sure point doesnt already exist
    for a in point_list:
        if a[0] == x and a[1] == y:
            exists = True
    return exists

def convert_to_grid(grid_chunk_width, grid_chunk_height, x, y):
    new_x = math.floor(x / grid_chunk_width)
    new_y = math.floor(y / grid_chunk_height)
    new_cord = (new_x, new_y)
    return new_cord

def draw_box_c(posx, posy, width, height, r, g, b, alpha):
    global window_width
    global window_height
    posx = float(posx)
    posy = float(posy)
    width = float(width)
    height = float(height)
    r = float(r)
    g = float(g)
    b = float(b)
    alpha = float(alpha)

    verticies = [
        posx - (width / 2), posy - (height / 2), 0.0,  ## Top Left
        posx - (width / 2) + width, posy - (height / 2), 0.0,  ## Top Right
        posx - (width / 2) + width, posy - (height / 2) + height, 0.0,  ## Bottom Right
        posx - (width / 2), posy - (height / 2) + height, 0.0  ## Bottom Left
    ]

    color = [
        r, g, b, alpha,
        r, g, b, alpha,
        r, g, b, alpha,
        r, g, b, alpha
    ]

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnable(GL_BLEND)
    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glColorPointer(4, GL_FLOAT, 0, color)
    glDrawArrays(GL_QUADS, 0, 4)
    glDisable(GL_BLEND)
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)

def draw_box(posx, posy, width, height, r, g, b, alpha):
    global window_width
    global window_height
    posx = float(posx)
    posy = float(posy)
    width = float(width)
    height = float(height)
    r = float(r)
    g = float(g)
    b = float(b)
    alpha = float(alpha)

    verticies = [
        posx,           posy, 0.0,            ## Top Left
        posx + width,   posy, 0.0,            ## Top Right
        posx + width,   posy + height, 0.0,   ## Bottom Right
        posx,           posy + height, 0.0    ## Bottom Left
    ]

    color = [
        r, g, b, alpha,
        r, g, b, alpha,
        r, g, b, alpha,
        r, g, b, alpha
    ]

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, verticies)
    glColorPointer(4, GL_FLOAT, 0, color)
    glDrawArrays(GL_QUADS, 0, 4)
    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)

