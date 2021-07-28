from tkinter import Tk, HIDDEN, NORMAL, Canvas
from turtle import fillcolor

def toggle_eyes():
    current_color = c.itemcget(eye_left, 'fill')
    new_color = c.body_color if current_color == 'white' else 'white'
    current_state = c.itemcget(pupil_left, 'state')
    new_state = NORMAL if current_state == HIDDEN else HIDDEN
    c.itemconfigure(pupil_left, state = new_state)
    c.itemconfigure(pupil_right, state = new_state)
    c.itemconfigure(eye_left, fill = new_color)
    c.itemconfigure(eye_right, fill = new_color)

def blink():
    toggle_eyes()
    win.after(250,toggle_eyes)
    win.after(3000,blink)

def toggle_pupils():
    if not c.crossed_eyes:
        c.move(pupil_left, 10,-5)
        c.move(pupil_right, -10,-5)
        c.crossed_eyes = True
    else:
        c.move(pupil_left, -10,5)
        c.move(pupil_right, 10,5)
        c.crossed_eyes = False

def toggle_tongue():
    if not c.tongue_out:
        c.itemconfigure(tongue_tip, state = NORMAL)
        c.itemconfigure(tongue_main, state = NORMAL)
        c.tongue_out = True
    else:
        c.itemconfigure(tongue_tip, state = HIDDEN)
        c.itemconfigure(tongue_main, state = HIDDEN)
        c.tongue_out = False

def cheeky(event):
    toggle_tongue()
    toggle_pupils()
    hide_happy(event)
    win.after(1000,toggle_tongue)
    win.after(1000,toggle_pupils)
    return

def show_happy(event):
    if(20 <= event.x and event.x < 350) and (20 <= event.y and event.y <= 350):
        c.itemconfigure(cheek_left, state = NORMAL)
        c.itemconfigure(cheek_right, state = NORMAL)
        c.itemconfigure(mouth_happy, state = NORMAL)
        c.itemconfigure(mouth_normal, state = HIDDEN)
        c.itemconfigure(mouth_sad, state = HIDDEN)
        c.happy_level = 10
    return

def hide_happy(event):
    c.itemconfigure(cheek_left, state = HIDDEN)
    c.itemconfigure(cheek_right, state = HIDDEN)
    c.itemconfigure(mouth_happy, state = HIDDEN)
    c.itemconfigure(mouth_normal, state = NORMAL)
    c.itemconfigure(mouth_sad, state = HIDDEN)   
    return    

def sad():
    if c.happy_level == 0:
        c.itemconfigure(mouth_happy, state = HIDDEN)
        c.itemconfigure(mouth_normal, state = HIDDEN)
        c.itemconfigure(mouth_sad, state = NORMAL)
    else:
        c.happy_level -= 1
    win.after(500,sad)

win = Tk()

c = Canvas(win, width=400, height=400)
c.configure(bg='dark blue', highlightthickness=0)

c.body_color = 'SkyBlue1'

body = c.create_oval(35,20,365,350, outline=c.body_color, fill=c.body_color)
foot_left = c.create_oval(65,320,145,360, outline=c.body_color, fill=c.body_color)
foot_left = c.create_oval(250,320,330,360, outline=c.body_color, fill=c.body_color)

ear_left = c.create_polygon(75,88,75,10,165,70, outline=c.body_color, fill=c.body_color)
ear_right = c.create_polygon(255,45,325,10,320,70, outline=c.body_color, fill=c.body_color)

eye_left = c.create_oval(130,110,160,170, outline='black', fill='white')
pupil_left = c.create_oval(140,145,150,155, outline='black', fill='black')
eye_right = c.create_oval(230,110,260,170, outline='black', fill='white')
pupil_right = c.create_oval(240,145,250,155, outline='black', fill='black')

mouth_normal = c.create_line(170,250,200,272,230,250, smooth=1, width=2, state=NORMAL)
mouth_happy = c.create_line(170,250,200,282,230,250, smooth=1, width=2, state=HIDDEN)
mouth_sad = c.create_line(170,250,200,232,230,250, smooth=1, width=2, state=HIDDEN)

tongue_main = c.create_rectangle(170,250,230,290, outline='red', fill='red', state=HIDDEN)
tongue_tip = c.create_oval(170,285,230,300, outline='red', fill='red', state=HIDDEN)

cheek_left = c.create_oval(70,180,120,230, outline='pink', fill='pink', state=HIDDEN)
cheek_right = c.create_oval(280,180,330,230, outline='pink', fill='pink', state=HIDDEN)

c.pack()

c.bind('<Motion>', show_happy)
c.bind('<Leave>', hide_happy)
c.bind('<Double-1>', cheeky)

c.crossed_eyes = False
c.tongue_out = False
c.happy_level = 10

win.after(1000,blink)
win.after(5000,sad)
win.mainloop()