import math
import utility
import os   
import glfw
import main
import time

mouse_x = 0
mouse_y = 0
mouse_action = 0

points = [
    []
]

drawing = False
deleting = False

r = 1
g = 1
b = 1

picker = True

pallet = [
    [1,0,0], [0,1,0], [0,0,1],
    [0.8,0,0],[0,0.8,0],[0,0,0.8],
    [0.6,0,0],[0,0.6,0],[0,0,0.6],
    [1,1,0],[0,1,1],[1,0,1],
    [0.8,0.8,0],[0,0.8,0.8],[0.8,0,0.8],
    [0.6,0.6,0],[0,0.6,0.6],[0.6,0,0.6],
    [1,0.4,0],[1,0,0.4],[0.25,0.25,0.25],
    [1,0.5,0],[1,0,0.5],[0.5,0.5,0.5],
    [1,0.6,0],[1,0,0.6],[0.75,0.75,0.75]
]

recent_colors = [(0,0,0),(0,0,0),(0,0,0)]

animate = False
state = 0  ## 0 = Drawing, 1 = Animating, 2 = Playing
current_frame = 0
onionskin = False

fps = 4
spf = 1/fps

def init(animate_i):
    global animate
    global onionskin
    global state
    global current_frame
    global recent_colors
    global pallet
    global picker
    global r
    global g
    global b
    global points
    points = [[]]
    r = 1
    g = 1
    b = 1
    picker = True
    pellet = [[1,0,0], [0,1,0], [0,0,1],[0.8,0,0],[0,0.8,0],[0,0,0.8],[0.6,0,0],[0,0.6,0],[0,0,0.6],[1,1,0],[0,1,1],[1,0,1],[0.8,0.8,0],[0,0.8,0.8],
             [0.8,0,0.8],[0.6,0.6,0],[0,0.6,0.6],[0.6,0,0.6],[1,0.4,0],[1,0,0.4],[0.25,0.25,0.25],[1,0.5,0],[1,0,0.5],[0.5,0.5,0.5],[1,0.6,0],[1,0,0.6],[0.75,0.75,0.75]]
    recent_colors = [(0,0,0),(0,0,0),(0,0,0)]
    current_frame = 0
    animate = animate_i
    if animate:
        state = 1
        onionskin = True
    if not animate:
        state = 0
        onionskin = False
        file_open_force("welcome")
    if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "@pallet.txt"):
        load_pallet()
    else:
        save_pallet()

def draw():
    if glfw.get_time() >= spf and state == 2:
        next_frame()

    if onionskin and state == 1:
        if len(points) > (current_frame + 1):
            for a in points[current_frame + 1]:
                utility.draw_box((a[0] * main.grid_chunk_width) + (main.grid_chunk_width / 5), a[1] * main.grid_chunk_height, main.grid_chunk_width / 5, main.grid_chunk_height, a[2], a[3], a[4], 0.0)
        if (current_frame - 1) >= 0:
            for a in points[current_frame - 1]:
                utility.draw_box(a[0] * main.grid_chunk_width, a[1] * main.grid_chunk_height, main.grid_chunk_width / 5, main.grid_chunk_height, a[2], a[3], a[4], 0.0)

    for a in points[current_frame]:
        utility.draw_box(a[0] * main.grid_chunk_width, a[1] * main.grid_chunk_height, main.grid_chunk_width, main.grid_chunk_height, a[2], a[3], a[4], 0.0)

    if picker:
        ## OUTLINE
        utility.draw_box(main.grid_chunk_width / 2, main.grid_chunk_height / 2, main.grid_chunk_width * 4, main.grid_chunk_height * 15, 1, 1, 1, 0.0)

        ## CURRENT COLOR
        utility.draw_box(main.grid_chunk_width, main.grid_chunk_height, main.grid_chunk_width*3, main.grid_chunk_height*2, r, g, b, 0.0)

        x = 1
        y = 4
        for color in pallet:
            utility.draw_box(main.grid_chunk_width*x, main.grid_chunk_height*y, main.grid_chunk_width, main.grid_chunk_height, color[0], color[1], color[2], 0.0)
            x = x+1
            if x >= 4:
                x = 1
                y = y+1
        
        x = 1
        y = y + 1
        for color in recent_colors:
            if x>=4:
                break
            utility.draw_box(main.grid_chunk_width*x, main.grid_chunk_height*y, main.grid_chunk_width, main.grid_chunk_height, color[0], color[1], color[2], 0.0)
            x = x+1
        
        if animate:
            ## OUTLINE
            utility.draw_box(main.grid_chunk_width / 2, main.window_height - (main.grid_chunk_height*4), main.grid_width * main.grid_chunk_width - main.grid_chunk_width, main.grid_chunk_height * 3, 1, 1, 1, 0.0)
            
            ## PLAY / PAUSE
            if state == 1:
                utility.draw_box(main.grid_chunk_width, main.window_height - (main.grid_chunk_height*3), main.grid_chunk_width, main.grid_chunk_height, 0, 0.8, 0, 0.0)
            else:
                utility.draw_box(main.grid_chunk_width, main.window_height - (main.grid_chunk_height*3), main.grid_chunk_width, main.grid_chunk_height, 0.8, 0, 0, 0.0)

            ## TIMELINE
            for i in range(len(points)):
                if (main.grid_width - 4) == i:
                    break
                elif current_frame == i:
                    utility.draw_box(main.grid_chunk_width * (i+3), main.window_height - (main.grid_chunk_height*3), main.grid_chunk_width, main.grid_chunk_height, 0, 0.5, 1, 0.0)
                elif i % 2:
                    utility.draw_box(main.grid_chunk_width * (i+3), main.window_height - (main.grid_chunk_height*3), main.grid_chunk_width, main.grid_chunk_height, 0.75, 0.75, 0.75, 0.0)
                else:
                    utility.draw_box(main.grid_chunk_width * (i+3), main.window_height - (main.grid_chunk_height*3), main.grid_chunk_width, main.grid_chunk_height, 0.5, 0.5, 0.5, 0.0)
                


def mouse_update_event(xpos, ypos, window):
    global mouse_x
    global mouse_y

    mouse_x = xpos
    mouse_y = ypos

    if r==0 and g==0 and b==0:
        return

    if drawing:
        gridx = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, xpos, ypos)[0]
        gridy = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, xpos, ypos)[1]
        if not utility.point_exists(points[current_frame],gridx,gridy):
            points[current_frame].append((gridx, gridy, r, g, b))
            glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if deleting:
        gridx = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, xpos, ypos)[0]
        gridy = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, xpos, ypos)[1]
        if utility.point_exists(points[current_frame],gridx,gridy):
            for a in points[current_frame]:
                if a[0] == gridx and a[1] == gridy:
                    points[current_frame].remove(a)
            glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

def mouse_click_event(window, button, action):
    global drawing
    global deleting
    global mouse_action
    global recent_colors

    if button == 0 and action == 1:
        if picker == True and mouse_x > (main.grid_chunk_width / 2) and mouse_x < (main.grid_chunk_width / 2) + (main.grid_chunk_width * 4) and mouse_y > (main.grid_chunk_height / 2) and mouse_y < (main.grid_chunk_height / 2) + (main.grid_chunk_height * 15):
            picker_clicked(0)
        else:
            if r==recent_colors[0][0] and g==recent_colors[0][1] and b==recent_colors[0][2]:
                pass
            else:
                for c in recent_colors:
                    if c[0] == r and c[1] == g and c[2] == b:
                        recent_colors.remove((r, g, b))
                recent_colors.insert(0, (r, g, b))
            drawing = True
            deleting = False

            gridx = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[0]
            gridy = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[1]
            if not utility.point_exists(points[current_frame],gridx,gridy) and not mouse_x == 0 and not mouse_y == 0:
                points[current_frame].append((gridx, gridy, r, g, b))
                glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if button == 0 and action == 0:
        drawing = False

    if button == 1 and action == 1:
        if picker == True and mouse_x > (main.grid_chunk_width / 2) and mouse_x < (main.grid_chunk_width / 2) + (main.grid_chunk_width * 4) and mouse_y > (main.grid_chunk_height / 2) and mouse_y < (main.grid_chunk_height / 2) + (main.grid_chunk_height * 15):
            picker_clicked(1)
        else:
            drawing = False
            deleting = True
            gridx = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[0]
            gridy = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[1]
            if utility.point_exists(points[current_frame],gridx,gridy):
                for a in points[current_frame]:
                    if a[0] == gridx and a[1] == gridy:
                        points[current_frame].remove(a)
                glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))
        
    if button == 1 and action == 0:
        deleting = False

def picker_clicked(button):
    global r
    global g
    global b

    gridx = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[0]
    gridy = utility.convert_to_grid(main.grid_chunk_width, main.grid_chunk_height, mouse_x, mouse_y)[1]

    if(button == 0):
        x = 1
        y = 4
        for color in pallet:
            if x >= 4:
                x = 1
                y = y+1
            if x == gridx and y == gridy:
                r = color[0]
                g = color[1]
                b = color[2]
            x = x+1

        y = y + 2
        x = 1
        for color in recent_colors:
            if x >= 4:
                break
            if x == gridx and y == gridy:
                r = color[0]
                g = color[1]
                b = color[2]
            x = x+1
    else:
        x = 1
        y = 4
        for color in pallet:
            if x >= 4:
                x = 1
                y = y+1
            if x == gridx and y == gridy:
                color[0] = r
                color[1] = g
                color[2] = b
            x = x+1
        save_pallet()
        


def key_press(window, key, action):
    global points
    global picker
    global current_frame
    global r
    global g
    global b

    if key == 258 and action == 1:
        if picker == True:
            picker = False
        else:
            picker = True

    if key == 49 and action == 1:
        r = 1
        g = 1
        b = 1
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 50 and action == 1:
        r = 1
        g = 0
        b = 0
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 51 and action == 1:
        r = 0
        g = 1
        b = 0
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 52 and action == 1:
        r = 0
        g = 0
        b = 1
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 54 and action == 1:
        r = 1
        g = 0.5
        b = 0
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 55 and action == 1:
        if r == 1:
            r = 0
        else:
            r = 1
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))
    
    if key == 56 and action == 1:
        if g == 1:
            g = 0
        else:
            g = 1
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 57 and action == 1:
        if b == 1:
            b = 0
        else:
            b = 1
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 66 and action == 1:
        if r >= 1:
            r = 0
        else:
            r = r+0.05
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))
    
    if key == 78 and action == 1:
        if g >= 1:
            g = 0
        else:
            g = g+0.05
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 77 and action == 1:
        if b >= 1:
            b = 0
        else:
            b = b+0.05
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 67 and action == 1:
        points[current_frame] = []
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 83 and action == 1:
        file_save()

    if key == 79 and action == 1:
        file_open()
        glfw.set_window_title(window, "Drawing! - Left click to place, right click to break - " + str(len(points[current_frame]) - 1) + " Pixels Drawn - Red: " + str(r) + ", Green: " + str(g) + ", Blue: " + str(b))

    if key == 44 and action == 1 and state == 1:
        previous_frame() ## <

    if key == 46 and action == 1 and state == 1:
        next_frame() ## >

    if key == 32 and action == 1 and animate:
        toggle_playing() ## Spacebar

    if key == 65 and action == 1 and state == 1:
        toggle_onion_skin() ## A

def file_save():
    print("$  ")
    print("$  We see that your are trying to save your Cody Draw(TM) project! ")
    print("$  Please type in the name you would like to give your project:")
    name = input("@  ")
    print("$  ")
    print("$  ")
    print("$  Saving your Cody Draw(TM) project as " + name)
    print("$  ")

    if animate:
        with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "files" + os.path.sep + "animations" + os.path.sep + "@" + str(name) + ".txt",mode = 'w',encoding = 'utf-8') as f:
            for a in points:
                for b in a:
                    f.write(str(b[0])+","+str(b[1])+","+str(b[2])+","+str(b[3])+","+str(b[4])+";")
                f.write("\n")
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "files" + os.path.sep + "drawings" + os.path.sep + "@" + str(name) + ".txt",mode = 'w',encoding = 'utf-8') as f:
            for a in points[current_frame]:
                f.write(str(a[0])+","+str(a[1])+","+str(a[2])+","+str(a[3])+","+str(a[4])+"\n")

def file_open():
    print("$  ")
    print("$  We see that your are trying to open a Cody Draw(TM) project! ")
    print("$  Please type in the name of the Cody Draw(TM) project you would like to open:")
    name = input("@  ")
    print("$  ")
    file_open_force(str(name))

def file_open_force(name):
    global points

    if animate:
        print("$  ")
        print("$  Opening the Cody Draw(TM) animation " + name)
        print("$  ")
        points = []
        i = 0
        with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "files" + os.path.sep + os.path.sep + "animations" + os.path.sep + "@" + str(name) + ".txt",mode = 'r',encoding = 'utf-8') as f:
            for line in f:
                line = str(line)
                line = line.split(';')
                line.remove('\n')
                points.append([])
                for a in line:
                    a = str(a)
                    a = a.split(',')
                    points[i].append((int(a[0]), int(a[1]), float(a[2]), float(a[3]), float(a[4])))
                i = i + 1
    else:
        if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "files" + os.path.sep + "drawings" + os.path.sep + "@" + str(name) + ".txt"):
            print("$  ")
            print("$  Opening the Cody Draw(TM) project " + name)
            print("$  ")
            points = [[]]
            with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "files" + os.path.sep + "drawings" + os.path.sep + "@" + str(name) + ".txt",mode = 'r',encoding = 'utf-8') as f:
                for line in f:
                    line = str(line)
                    line = line.split(',')
                    for a in line:
                        a = a.replace('\n', '')
                    points[current_frame].append((int(line[0]), int(line[1]), float(line[2]), float(line[3]), float(line[4])))
        else:
            print("$  ")
            print("$  Were sorry but Cody Draw(TM) could not find the project " + name)
            print("$  ")

def save_pallet():
    with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "@pallet.txt",mode = 'w',encoding = 'utf-8') as f:
        for a in pallet:
            f.write(str(a[0])+","+str(a[1])+","+str(a[2])+"\n")

def load_pallet():
    global pallet
    pallet = []
    with open(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "@pallet.txt",mode = 'r',encoding = 'utf-8') as f:
        for line in f:
            line = str(line)
            line = line.split(',')
            for a in line:
                a = a.replace('\n', '')
            pallet.append([float(line[0]), float(line[1]), float(line[2])])

def next_frame():
    global current_frame

    if state == 1:
        if len(points) > (current_frame + 1):
            current_frame = current_frame + 1
        else:
            points.append([])
            current_frame = current_frame + 1
    elif state == 2:
        glfw.set_time(0.0)
        if len(points) > (current_frame + 1):
            current_frame = current_frame + 1
        else:
            current_frame = 0

def previous_frame():
    global current_frame

    if state == 1 and not current_frame <= 0:
        current_frame = current_frame - 1

def toggle_playing():
    global state

    if state == 1:
        state = 2
        glfw.set_time(0.0)
    elif state == 2:
        state = 1

def toggle_onion_skin():
    global onionskin
    if state == 1:
        if onionskin == True:
            onionskin = False
        else:
            onionskin = True