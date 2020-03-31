import math
import utility

button_width = 0
button_height = 0

mouse_x = 0
mouse_y = 0

hover = 0

def draw(window_width, window_height):
    global button_width
    global button_height
    global hover

    button_width = window_width * 0.25
    button_height = window_height * 0.075

    if mouse_x > (window_width / 2) - (button_width / 2) and mouse_x < (window_width / 2) - (button_width / 2) + button_width:
        left_dash_x = (window_width / 2) - (button_width / 2) - 15
        right_dash_x = (window_width / 2) + (button_width / 2) + 5

        if mouse_y > (window_height / 2) * 0.8 - (button_height / 2) and mouse_y < (window_height / 2) * 0.8 - (button_height / 2) + button_height:
            utility.draw_box(left_dash_x, (window_height / 2) * 0.8 - (button_height / 2), 10, button_height, 1, 1, 1, 0)
            utility.draw_box(right_dash_x, (window_height / 2) * 0.8 - (button_height / 2), 10, button_height, 1, 1, 1, 0)
            hover = 1
        elif mouse_y > (window_height / 2) - (button_height / 2) and mouse_y < (window_height / 2) - (button_height / 2) + button_height:
            utility.draw_box(left_dash_x, (window_height / 2) - (button_height / 2), 10, button_height, 1, 1, 1, 0)
            utility.draw_box(right_dash_x, (window_height / 2) - (button_height / 2), 10, button_height, 1, 1, 1, 0)
            hover = 2
        elif mouse_y > (window_height / 2) * 1.2 - (button_height / 2) and mouse_y < (window_height / 2) * 1.2 - (button_height / 2) + button_height:
            utility.draw_box(left_dash_x, (window_height / 2) * 1.2 - (button_height / 2), 10, button_height, 1, 0, 0, 0)
            utility.draw_box(right_dash_x, (window_height / 2) * 1.2 - (button_height / 2), 10, button_height, 1, 0, 0, 0)
            hover = 3
        else:
            hover = 0
    else:
        hover = 0
        

    utility.draw_box_c(window_width / 2, (window_height / 2) * 0.8, button_width, button_height, 1, 1, 1, 0.0)
    utility.draw_box_c(window_width / 2, window_height / 2, button_width, button_height, 1, 1, 1, 0.0)
    utility.draw_box_c(window_width / 2, (window_height / 2) * 1.2, button_width, button_height, 1, 0, 0, 0.0)

def mouse_update_event(xpos, ypos):
    global mouse_x
    global mouse_y

    mouse_x = xpos
    mouse_y = ypos

def mouse_click_event(button):
    if hover == 1:
        return 2
    elif hover == 2:
        return 3
    elif hover == 3:
        return 4
    else:
        return 1