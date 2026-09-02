import sys
import tkinter as tk
from tkinter import messagebox

def parse_infix(infix_str: str) -> str:
    """Insert spaces between digits, operators, and parentheses for tokenization."""
    ret = ""
    infix_str = infix_str.strip()
    for i, tmp in enumerate(infix_str):
        if tmp == '.' or tmp.isdigit():
            ret += tmp
            if i < len(infix_str) - 1:
                if not infix_str[i + 1].isdigit() and infix_str[i + 1] != '.':
                    ret += " "
        elif tmp in "+-*/()":
            ret += tmp + " "
        elif tmp == ' ':
            continue
        else:
            ret += tmp + " "
    return ret.strip()

def convert_to_postfix(infix: str) -> str:
    """Convert space-separated infix expression string to postfix (RPN) notation."""
    ret = ""
    infix_arr = [token for token in infix.strip().split(' ') if token]
    s = []

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in infix_arr:
        if token == "(":
            s.append(token)
        elif token in precedence:
            curr_prec = precedence[token]
            while s and s[-1] in precedence and precedence[s[-1]] >= curr_prec:
                ret += s.pop() + " "
            s.append(token)
        elif token == ")":
            while s and s[-1] != "(":
                ret += s.pop() + " "
            if s and s[-1] == "(":
                s.pop()
        else:
            ret += token + " "

    while s:
        top = s.pop()
        if top not in "()":
            ret += top + " "

    return ret.strip()

def calculate_postfix(postfix: str) -> str:
    """Evaluate postfix expression string and return numeric result string."""
    postfix = postfix.strip()
    if not postfix:
        return "0"

    postfix_arr = [token for token in postfix.split(' ') if token]
    s = []

    for token in postfix_arr:
        if token in ["+", "-", "*", "/"]:
            if len(s) < 2:
                raise ValueError(f"Invalid postfix expression: insufficient operands for operator '{token}'")
            b = s.pop()
            a = s.pop()
            if token == "+":
                s.append(a + b)
            elif token == "-":
                s.append(a - b)
            elif token == "*":
                s.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                s.append(a / b)
        else:
            try:
                s.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid token '{token}' in expression")

    if len(s) != 1:
        raise ValueError("Invalid expression evaluation")

    res = s.pop()
    return str(int(res)) if res.is_integer() else f"{res:.4f}".rstrip('0').rstrip('.')

def evaluate_infix(infix_expression: str) -> tuple:
    """Parse, convert, and evaluate an infix math expression."""
    temp_infix = parse_infix(infix_expression)
    postfix_expr = convert_to_postfix(temp_infix)
    result_val = calculate_postfix(postfix_expr)
    return temp_infix, postfix_expr, result_val

def run_gui():
    root = tk.Tk()
    root.title("Infix to Postfix Calculator")
    root.geometry("340x350")

    app = tk.Frame(root)
    app.pack(padx=20, pady=20)

    lbl = tk.Label(app, text="Infix / Postfix Calculator", font=("Helvetica", 14, "bold"))
    lbl.pack(pady=5)

    lbl_infix = tk.Label(app, text="Infix Expression (e.g. 3 + 4 * 2 / ( 1 - 5 )):")
    lbl_infix.pack()
    infix_entry = tk.Entry(app, width=30)
    infix_entry.pack(pady=3)

    lbl_tempinfix = tk.Label(app, text="Parsed Infix Tokens:")
    lbl_tempinfix.pack()
    tempinfix_entry = tk.Entry(app, width=30)
    tempinfix_entry.pack(pady=3)

    lbl_postfix = tk.Label(app, text="Postfix (RPN):")
    lbl_postfix.pack()
    postfix_entry = tk.Entry(app, width=30)
    postfix_entry.pack(pady=3)

    lbl_result = tk.Label(app, text="Result:")
    lbl_result.pack()
    result_entry = tk.Entry(app, width=30)
    result_entry.pack(pady=3)

    def calculate():
        infix_str = infix_entry.get()
        if not infix_str.strip():
            messagebox.showwarning("Empty Input", "Please enter an infix expression.")
            return
        try:
            temp_infix, postfix_str, result_str = evaluate_infix(infix_str)
            tempinfix_entry.delete(0, tk.END)
            tempinfix_entry.insert(0, temp_infix)
            postfix_entry.delete(0, tk.END)
            postfix_entry.insert(0, postfix_str)
            result_entry.delete(0, tk.END)
            result_entry.insert(0, result_str)
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    btn = tk.Button(app, text="Calculate", bg="#2ECC71", fg="white", font=("Helvetica", 10, "bold"), command=calculate)
    btn.pack(pady=10)

    root.mainloop()

def main():
    run_gui()

if __name__ == '__main__':
    main()