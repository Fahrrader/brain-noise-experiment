from tkinter import *
from os import mkdir, path
import threading
import random
import datetime


class Cube:
    def __init__(self, index, alpha):
        self.index = index
        self.alpha = alpha
        self.left_clicks = 0
        self.right_clicks = 0


def fill_cubes():
    cubes.clear()
    experiments.clear()
    times_show.clear()
    times_break.clear()
    for i in range(different_cubes):
        experiments.append(Cube(i, int(255 * i / 15)))
        for j in range(instance_cubes):
            cubes.append(experiments[i])
            times_show.append(time_show_min + random.random() * time_break_range)
            times_break.append(time_break_min + random.random() * time_break_range)
    random.shuffle(cubes)
    random.shuffle(times_show)
    random.shuffle(times_break)


folder = "results"

if not path.exists(folder):
    mkdir(folder)

width = 400
height = 520

time_show_min = 0.5
time_show_range = 0.2
time_break_min = 1.5
time_break_range = 0.5
times_show = []
times_break = []

current_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")

different_cubes = 16
instance_cubes = 47
cubes = []
experiments = []
current_cube = []

cube_width = 160
line_thickness = 3

red_size = 8
red_thickness = 1
red_light = "red"


# alpha must be of 0-255
def change_left_alpha(alpha):
    for line in static_lines:
        canvas.itemconfig(line, fill="black")
    for line in cross_lines:
        canvas.itemconfig(line, fill=red_light)

    color = hex(alpha)[2:]
    fill = "#%s%s%s" % (color, color, color)
    canvas.itemconfig(illusion_right_lower, fill=fill)
    canvas.itemconfig(illusion_right_upper, fill=fill)
    canvas.itemconfig(illusion_right_left, fill=fill)

    color = hex(255 - alpha)[2:]
    fill = "#%s%s%s" % (color, color, color)
    canvas.itemconfig(illusion_left_upper, fill=fill)
    canvas.itemconfig(illusion_left_lower, fill=fill)
    canvas.itemconfig(illusion_left_right, fill=fill)

    if alpha < 128:
        canvas.tag_lower(illusion_left_upper)
        canvas.tag_lower(illusion_left_lower)
        canvas.tag_lower(illusion_left_right)
    else:
        canvas.tag_lower(illusion_right_lower)
        canvas.tag_lower(illusion_right_upper)
        canvas.tag_lower(illusion_right_left)


def hide_canvas():
    canvas.itemconfig(illusion_left_upper, fill="white")
    canvas.itemconfig(illusion_left_lower, fill="white")
    canvas.itemconfig(illusion_left_right, fill="white")
    canvas.itemconfig(illusion_right_lower, fill="white")
    canvas.itemconfig(illusion_right_upper, fill="white")
    canvas.itemconfig(illusion_right_left, fill="white")
    for line in static_lines:
        canvas.itemconfig(line, fill="white")
    for line in cross_lines:
        canvas.itemconfig(line, fill="white")


def save_data():
    print("hey")
    filename = ("%s %s.txt" % (name.get().strip(), current_time)).strip()
    file = open("%s\%s" % (folder, filename), "w")

    for i in experiments:
        click_relation = "NaN"
        if i.left_clicks + i.right_clicks != 0:
            click_relation = "%.3f" % (i.left_clicks / (i.left_clicks + i.right_clicks))

        file.write("%s\t%s\t%s\n" % (i.index,
                                     "%.3f" % (i.alpha / 255 - 0.5),
                                     click_relation))


def change_cube():
    if len(cubes) % int(different_cubes / 2) == 0 and len(cubes) != different_cubes * instance_cubes:
        save_data()

    if len(cubes) == 0:
        hide_canvas()
        return

    label_start.config(text="Once your name is entered, press Enter/Return. You will see %s cubes\n"
                            "You will have about %s seconds to see a cube, and %s seconds to answer"
                            % (len(cubes), time_show_min + time_show_range / 2, time_break_min + time_break_range / 2))

    if len(current_cube) > 0:
        current_cube.pop(0)

    current_cube.append(cubes.pop(len(cubes) - 1))
    change_left_alpha(current_cube[0].alpha)

    t_show = threading.Timer(times_show[len(cubes)], hide_canvas)
    t_show.start()
    t_break = threading.Timer(times_break[len(cubes)]+times_show[len(cubes)], change_cube)
    t_break.start()


def select_orientation(answer):
    if len(current_cube) == 0:
        return

    sign = 1
    if answer == 'left':
        sign = -1
        current_cube[0].left_clicks += 1
    elif answer == 'right':
        current_cube[0].right_clicks += 1
    else:
        return

    if sign * (current_cube[0].alpha / 255 - 0.5) >= 0:
        print("sounds about right")
    else:
        print("not really")

    current_cube.pop(0)


def select_key(event):
    if event.keysym.lower() == 'return':
        global current_time
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        name.configure(state=DISABLED)
        fill_cubes()
        change_cube()
    else:
        select_orientation(event.keysym.lower())


def select_left_button(event):
    select_orientation('left')


def select_right_button(event):
    select_orientation('right')


win = Tk()
win.title("Experiment")

win.geometry("%dx%d" % (width, height))
win.minsize(width, height)
win.bind("<Key>", select_key)

canvas = Canvas(win, width=width, height=width)
canvas.config(background="white")
canvas.pack()

label_arrows = Label(win, text="Use arrow keys ← and → to select orientation of the cube, or these buttons:")
label_arrows.pack()

frame_buttons = Frame(win)
frame_buttons.pack()

button_left = Button(frame_buttons, text="Left", width=10)
button_left.bind("<Button-1>", select_left_button)
button_left.pack(side=LEFT)

button_right = Button(frame_buttons, text="Right", width=10)
button_right.bind("<Button-1>", select_right_button)
button_right.pack(side=RIGHT)

label_start = Label(win, text="Once your name is entered, press Enter/Return. You will see %s cubes\n"
                              "You will have about %s seconds to see a cube, and %s seconds to answer"
                              % (different_cubes * instance_cubes,
                                 time_show_min+time_show_range / 2, time_break_min+time_break_range/2))
label_start.pack(side=BOTTOM)

name = Entry(win, width=50)
name.focus_set()
name.pack(side=BOTTOM)

illusion_left_upper = canvas.create_line(160, 240, 160, 80, width=line_thickness)
illusion_left_lower = canvas.create_line(160, 240, 80, 320, width=line_thickness)
illusion_left_right = canvas.create_line(160, 240, 320, 240, width=line_thickness)

illusion_right_lower = canvas.create_line(240, 160, 80, 160, width=line_thickness)
illusion_right_upper = canvas.create_line(240, 160, 320, 80, width=line_thickness)
illusion_right_left = canvas.create_line(240, 160, 240, 320, width=line_thickness)

# static block
static_lines = [
    canvas.create_line(width / 2 - cube_width * 1.5 / 2, 160, 80, 320, width=line_thickness),
    canvas.create_line(80, 160, 160, 80, width=line_thickness),
    canvas.create_line(80, 320, 240, 320, width=line_thickness),
    canvas.create_line(160, 80, 320, 80, width=line_thickness),
    canvas.create_line(320, 80, 320, 240, width=line_thickness),
    canvas.create_line(320, 240, 240, 320, width=line_thickness),
]

cross_lines = [
    canvas.create_line(width / 2 - red_size / 2, width / 2,
                       width / 2 + red_size / 2, width / 2, width=red_thickness, fill=red_light),
    canvas.create_line(width / 2, width / 2 - red_size / 2,
                       width / 2, width / 2 + red_size / 2, width=red_thickness, fill=red_light)
]

hide_canvas()

win.mainloop()
