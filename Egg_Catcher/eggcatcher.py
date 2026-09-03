import sys
from itertools import cycle
from random import randrange
import tkinter as tk
from tkinter import Tk, Canvas, messagebox

class EggCatcherGame:
    def __init__(self, root: Tk = None):
        self.win = root or Tk()
        self.win.title("Egg Catcher Game")
        self.win.resizable(width=False, height=False)

        self.canvas_width = 800
        self.canvas_height = 400

        self.c = Canvas(self.win, width=self.canvas_width, height=self.canvas_height, background='deep sky blue')
        self.c.create_rectangle(-5, self.canvas_height - 100, self.canvas_width + 5, self.canvas_height + 5, fill='sea green', width=0)
        self.c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
        self.c.pack()

        self.color_cycle = cycle(['light blue', 'light pink', 'light yellow', 'light green', 'red', 'blue', 'green', 'black'])
        self.egg_width = 45
        self.egg_height = 55
        self.egg_score = 10
        self.egg_speed = 500
        self.egg_interval = 4000
        self.difficulty_factor = 0.95

        self.catcher_color = 'blue'
        self.catcher_width = 100
        self.catcher_height = 100
        self.catcher_start_x = self.canvas_width / 2 - self.catcher_width / 2
        self.catcher_start_y = self.canvas_height - self.catcher_height - 20

        self.catcher = self.c.create_arc(
            self.catcher_start_x, self.catcher_start_y,
            self.catcher_start_x + self.catcher_width, self.catcher_start_y + self.catcher_height,
            start=200, extent=140, style='arc', outline=self.catcher_color, width=3
        )

        self.score = 0
        self.score_text = self.c.create_text(10, 10, anchor='nw', font=('Arial', 18, 'bold'), fill='darkblue', text='Score : 0')

        self.lives_remaning = 3
        self.lives_text = self.c.create_text(self.canvas_width - 10, 10, anchor='ne', font=('Arial', 18, 'bold'), fill='darkblue', text='Lives : 3')

        self.eggs = []
        self.game_running = True

        self.c.bind('<Left>', self.move_left)
        self.c.bind('<Right>', self.move_right)
        self.c.focus_set()

    def start(self):
        self.win.after(1000, self.create_eggs)
        self.win.after(1000, self.move_eggs)
        self.win.after(1000, self.catch_check)
        self.win.mainloop()

    def create_eggs(self):
        if not self.game_running:
            return
        x = randrange(10, 740)
        y = 40
        new_egg = self.c.create_oval(x, y, x + self.egg_width, y + self.egg_height, fill=next(self.color_cycle), width=0)
        self.eggs.append(new_egg)
        self.win.after(self.egg_interval, self.create_eggs)

    def move_eggs(self):
        if not self.game_running:
            return
        to_drop = []
        for egg in list(self.eggs):
            coords = self.c.coords(egg)
            if coords and len(coords) == 4:
                _, _, _, egg_y2 = coords
                self.c.move(egg, 0, 10)
                if egg_y2 > self.canvas_height:
                    to_drop.append(egg)

        for egg in to_drop:
            self.egg_dropped(egg)

        self.win.after(self.egg_speed, self.move_eggs)

    def egg_dropped(self, egg):
        if egg in self.eggs:
            self.eggs.remove(egg)
            self.c.delete(egg)
            self.lose_a_life()

    def lose_a_life(self):
        self.lives_remaning -= 1
        self.c.itemconfigure(self.lives_text, text='Lives : ' + str(self.lives_remaning))
        if self.lives_remaning == 0:
            self.game_running = False
            response = messagebox.askyesno('GAME OVER!', 'Final Score: ' + str(self.score) + '\nDo you want to play again?')
            if response:
                self.reset_game()
            else:
                self.win.destroy()

    def reset_game(self):
        for egg in self.eggs:
            self.c.delete(egg)
        self.eggs = []
        self.score = 0
        self.lives_remaning = 3
        self.egg_speed = 500
        self.egg_interval = 4000
        self.game_running = True
        self.c.itemconfigure(self.score_text, text='Score : ' + str(self.score))
        self.c.itemconfigure(self.lives_text, text='Lives : ' + str(self.lives_remaning))
        self.win.after(1000, self.create_eggs)
        self.win.after(1000, self.move_eggs)
        self.win.after(1000, self.catch_check)

    def catch_check(self):
        if not self.game_running:
            return
        catcher_coords = self.c.coords(self.catcher)
        if catcher_coords and len(catcher_coords) == 4:
            c_x, c_y, c_x2, c_y2 = catcher_coords
            caught_list = []
            for egg in list(self.eggs):
                egg_coords = self.c.coords(egg)
                if egg_coords and len(egg_coords) == 4:
                    e_x, e_y, e_x2, e_y2 = egg_coords
                    if c_x < e_x and e_x2 < c_x2 and c_y2 - e_y2 < 40:
                        caught_list.append(egg)

            for egg in caught_list:
                if egg in self.eggs:
                    self.eggs.remove(egg)
                    self.c.delete(egg)
                    self.increase_score(self.egg_score)

        self.win.after(100, self.catch_check)

    def increase_score(self, points):
        self.score += points
        self.egg_speed = max(int(self.egg_speed * self.difficulty_factor), 50)
        self.egg_interval = max(int(self.egg_interval * self.difficulty_factor), 500)
        self.c.itemconfigure(self.score_text, text='Score : ' + str(self.score))

    def move_left(self, event):
        coords = self.c.coords(self.catcher)
        if coords and coords[0] > 0:
            self.c.move(self.catcher, -20, 0)

    def move_right(self, event):
        coords = self.c.coords(self.catcher)
        if coords and coords[2] < self.canvas_width:
            self.c.move(self.catcher, 20, 0)

def main():
    game = EggCatcherGame()
    game.start()

if __name__ == '__main__':
    main()

