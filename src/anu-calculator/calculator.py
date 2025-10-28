import tkinter as tk
from tkinter import messagebox
import ast
import operator as op

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.geometry("420x500")
        self.resizable(False, False)

        self.create_widgets()

    # --- Safe expression evaluator (no eval()) ---
    
    def safe_eval(self, expr):
        allowed_ops = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow
        }

        def _eval(node):
            if isinstance(node, ast.Num):  # number
                return node.n
            elif isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
                return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
            else:
                raise ValueError("Invalid Expression")

        try:
            parsed = ast.parse(expr, mode='eval').body
            return _eval(parsed)
        except Exception:
            raise ValueError("Invalid Expression")

    # --- GUI setup ---
    def create_widgets(self):
        self.entry = tk.Entry(self, font=("Arial", 20), borderwidth=5, relief="sunken", justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10, ipady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ]

        for (text, row, col) in buttons:
            if text == '=':
                btn = tk.Button(self, text=text, width=5, height=2, font=("Arial", 18),
                                bg="#4CAF50", fg="white", command=self.calculate)
            else:
                btn = tk.Button(self, text=text, width=5, height=2, font=("Arial", 18),
                                command=lambda t=text: self.append_char(t))
            btn.grid(row=row, column=col, padx=5, pady=5)

        tk.Button(self, text='C', width=5, height=2, font=("Arial", 18),
                  bg="#f44336", fg="white", command=self.clear).grid(row=5, column=0, padx=5, pady=5)

        tk.Button(self, text='⌫', width=5, height=2, font=("Arial", 18),
                  bg="#ff9800", fg="white", command=self.backspace).grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self, text='Exit', width=11, height=2, font=("Arial", 18),
                  bg="#607d8b", fg="white", command=self.quit).grid(row=5, column=2, columnspan=2, padx=5, pady=5)

        # Keyboard bindings
        self.bind('<Return>', lambda e: self.calculate())
        self.bind('<BackSpace>', lambda e: self.backspace())
        for key in "0123456789+-*/.":
            self.bind(key, lambda e, k=key: self.append_char(k))

    # --- Button functions ---
    def append_char(self, char):
        self.entry.insert(tk.END, char)

    def clear(self):
        self.entry.delete(0, tk.END)

    def backspace(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current[:-1])

    def calculate(self):
        try:
            expression = self.entry.get()
            result = self.safe_eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")

if __name__ == "__main__":
    Calculator().mainloop()
