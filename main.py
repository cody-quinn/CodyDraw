import glfw
import utility
import math
import os
import mainmenu
import draw
from OpenGL.GL import *
from OpenGL.GLU import *

##### WARNING ---- CHANGING THESE VALUES MAY EFFECT THE OUTCOME OF SAVED IMAGES #####

window_width = 1280  ## Change this number to change the width of the screen
window_height = 720  ## Change this number to hange the height of the screen 

grid_chunk_width = 40  ## Change this number to change the width of the pixels
grid_chunk_height = 20  ## Change this number to change the height of the pixels

debug = False  ## Toggle debug mode, will cause spam in console

grid_width = int(math.ceil(window_width / grid_chunk_width))
grid_height = int(math.ceil(window_height / grid_chunk_height))

#### END

mode = 1 ## 1 == Main Menu, 2 == Drawing, 3 == Animating, 4 == Quit

def main():
    global window
    global mode

    print("$  ")
    print("$   Welcome to Cody Draw(TM)!")
    print("$  ")
    print("$   Cody draw is very simple to use, here is a list of all the controls")
    print("$      - Press & Drag 'Left Mouse Button' to draw")
    print("$      - Press & Drag 'Right Mouse Button' to erase")
    print("$      - Press 'tab' to toggle the UI (color picker, timeline, exc)")
    print("$      - Press 'c' to clear the canvas / frame")
    print("$      - Press 's' to save your work")
    print("$      - Press 'o' to open saved work")
    print("$      - Press 'e' to export your work into a PNG")
    print("$      - Press '1' to draw in the color white")
    print("$      - Press '2' to draw in the color red")
    print("$      - Press '3' to draw in the color green")
    print("$      - Press '4' to draw in the color blue")
    print("$      - Press '6' to draw in the color orange")
    print("$   ")
    print("$   These next controls might get a little bit complicated, they will allow you to mix colors")
    print("$   You can see your RGB color value in the title, its 3 numbers valued at 0 - 1 in order")
    print("$      - Press '7' to toggle the color blue")
    print("$      - Press '8' to toggle the color green")
    print("$      - Press '9' to toggle the color red")
    print("$      - Press 'b' to increase the red value by 0.05")
    print("$      - Press 'n' to increase the green value by 0.05")
    print("$      - Press 'm' to increase the blue value by 0.05")
    print("$  ")
    print("$  When animating these additional keybinds exist")
    print("$      - Press 'space' to play/pause")
    print("$      - Press '>' to goto the next frame, or create another frame if one doesnt exist")
    print("$      - Press '<' to goto the previous frame")
    print("$      - Press 'a' to toggle the onionskin (preview of the previous frame / next frame)")
    print("$  ")
    print("$   There are a few example paintings bundled with your copy of Cody Draw(TM)")
    print("$   Access them using the 'o' keybind to open a Cody Draw(TM) file")
    print("$      - 'welcome'")
    print("$      - 'earth'")
    print("$      - 'intheair'")
    print("$      - 'chart'")
    print("$      - 'colors'")
    print("$  ")

    if not glfw.init():
        return
    
    window = glfw.create_window(window_width, window_height, "Welcome to Cody Draw(TM)", None, None)
    glfw.set_window_size_limits(window, window_width, window_height, window_width, window_height)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    glfw.make_context_current(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, window_height, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT)

    while not glfw.window_should_close(window):
        # Rendering
        glClear(GL_COLOR_BUFFER_BIT)

        if mode == 1:
            mainmenu.draw(window_width, window_height)
        elif mode == 2:
            draw.draw()
        elif mode == 3:
            draw.draw()
        
        # Other
        glfw.swap_buffers(window)
        glfw.poll_events()

    print("$  ")
    print("$  Cody Draw(TM) has been terminated!")
    print("$  Goodbye!")
    print("$  ")
    
    glfw.terminate()

def key_callback(window, key, scancode, action, mods):
    global mode

    if key == 256 and action == 1:
        mode = 1

    if mode == 2 or mode == 3:
        draw.key_press(window, key, action)

def cursor_position_callback(window, xpos, ypos):
    global mode

    if mode == 1:
        mainmenu.mouse_update_event(xpos, ypos)
    elif mode == 2 or mode == 3:
        draw.mouse_update_event(xpos, ypos, window)

def mouse_button_callback(window, button, action, mods):
    global drawing
    global deleting
    global mode

    if mode == 1:
        mode = mainmenu.mouse_click_event(button)
        if mode == 2:
            draw.init(False)
        elif mode == 3:
            draw.init(True)
        elif mode == 4:
            glfw.set_window_should_close(window, 1)
    elif mode == 2 or mode == 3:
        draw.mouse_click_event(window, button, action)

if __name__ == "__main__":
    main()
