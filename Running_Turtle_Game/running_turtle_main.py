from turtle import Turtle, Screen
import random
from tkinter import messagebox
from tkinter import *

FONT = ("Arial", 20, "normal")

screen = Screen()
screen.setup(width=500, height=400)
tim = Turtle()
tim.penup()
tim.hideturtle()
tim.goto(x=230, y=-200)
tim.setheading(90)
tim.pendown()
tim.pensize(3)
tim.pencolor()
tim.forward(400)
user_bet = screen.textinput(title="Make your bet",
                            prompt="Which turtle will win the race? Select a color (red, orange, yellow, green, blue, purple) ")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
is_race_on = False

all_turtles = []

for turtle_index in range(0, 6):
    y = -100
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y + 40 * turtle_index)
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True

while is_race_on:

    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is winner!")
                window = Tk()
                window.geometry("100x100")
                messagebox.showinfo("information", f"You've won! The {winning_color} turtle is winner!")
                window.destroy()

            else:
                print(f"You've lost! The {winning_color} turtle is winner!")
                window = Tk()
                window.geometry("100x100")
                messagebox.showinfo("information", f"You've lost! The {winning_color} turtle is winner!")
                window.destroy()

        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()