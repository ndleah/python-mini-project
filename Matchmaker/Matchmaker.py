import random
import sys
import tkinter as tk
from tkinter import Tk, Button

class MatchmakerGame:
    def __init__(self, root: Tk = None):
        self.root = root or Tk()
        self.root.title('Matchmaker Memory Game')
        self.root.resizable(width=False, height=False)

        self.first = True
        self.previousx = 0
        self.previousy = 0
        self.buttons = {}
        self.button_symbols = {}
        self.matches_found = 0
        self.is_busy = False

        self.symbols = [
            '✂', '✅', '✈', '✉', '✊', '✋', '✌', '✏', '✒', '✔', '✖', '✨',
            '✂', '✅', '✈', '✉', '✊', '✋', '✌', '✏', '✒', '✔', '✖', '✨'
        ]
        random.shuffle(self.symbols)

        for x in range(6):
            for y in range(4):
                btn = Button(
                    self.root,
                    text=' ',
                    command=lambda x=x, y=y: self.show_symbol(x, y),
                    width=10,
                    height=4,
                    font=('Arial', 14, 'bold')
                )
                btn.grid(column=x, row=y, padx=2, pady=2)
                self.buttons[x, y] = btn
                self.button_symbols[x, y] = self.symbols.pop()

    def show_symbol(self, x: int, y: int):
        if self.is_busy or self.buttons[x, y]['state'] == 'disabled':
            return

        self.buttons[x, y]['text'] = self.button_symbols[x, y]

        if self.first:
            self.previousx = x
            self.previousy = y
            self.first = False
        elif self.previousx != x or self.previousy != y:
            if self.button_symbols[self.previousx, self.previousy] != self.button_symbols[x, y]:
                self.is_busy = True
                self.root.after(500, self.reset_mismatched, x, y)
            else:
                self.buttons[self.previousx, self.previousy]['state'] = 'disabled'
                self.buttons[x, y]['state'] = 'disabled'
                self.matches_found += 1
                if self.matches_found == 12:
                    print("🎉 Game Over! All 12 pairs matched!")
                self.first = True

    def reset_mismatched(self, x: int, y: int):
        self.buttons[self.previousx, self.previousy]['text'] = ' '
        self.buttons[x, y]['text'] = ' '
        self.first = True
        self.is_busy = False

    def run(self):
        self.root.mainloop()

def main():
    game = MatchmakerGame()
    game.run()

if __name__ == '__main__':
    main()