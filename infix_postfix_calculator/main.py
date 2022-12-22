def parse_infix(input):
    ret = ""
    for i, tmp in enumerate(input):
        if tmp == '.':
            ret += tmp
        elif tmp.isdigit():
            ret += tmp
            if i < len(input) - 1:
                if not input[i + 1].isdigit() and input[i + 1] != '.':
                    ret += " "
        else:
            ret += tmp + " "
    return ret


def convert_to_postfix(infix):
    ret = ""
    infix = infix.strip()
    infix_arr = infix.split(' ')
    s = []
    for token in infix_arr:
        if token == "(":
            s.append(token)
        elif token == "+":
            while s and s[-1] in ["+", "-", "*", "/"]:
                ret += s.pop() + " "
            s.append(token)
        elif token == "-":
            while s and s[-1] in ["+", "-", "*", "/"]:
                ret += s.pop() + " "
            s.append(token)
        elif token == "*":
            while s and s[-1] in ["*", "/"]:
                ret += s.pop() + " "
            s.append(token)
        elif token == "/":
            while s and s[-1] in ["*", "/"]:
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
        ret += s.pop() + " "
    return ret


def calculate_postfix(postfix):
    ret = ""
    s = []
    postfix = postfix.strip()
    postfix_arr = postfix.split(' ')
    for token in postfix_arr:
        if token in ["+", "-", "*", "/"]:
            b = s.pop()
            a = s.pop()
            if token == "+":
                s.append(a + b)
            elif token == "-":
                s.append(a - b)
            elif token == "*":
                s.append(a * b)
            elif token == "/":
                s.append(a / b)
        else:
            s.append(float(token))
    ret = str(s.pop())
    return ret

from tkinter import *

root = Tk()
root.title("Calculator")
root.geometry("300x300")

app = Frame(root)
app.pack()

lbl = Label(app, text="Calculator")
lbl.pack()

lbl_infix = Label(app, text="Infix")
lbl_infix.pack()
infix = Entry(app)
infix.pack()

lbl_tempinfix = Label(app, text="Temp Infix")
lbl_tempinfix.pack()
tempinfix = Entry(app)
tempinfix.pack()

lbl_postfix = Label(app, text="Postfix")
lbl_postfix.pack()
postfix = Entry(app)
postfix.pack()

lbl_result = Label(app, text="Result")
lbl_result.pack()
result = Entry(app)
result.pack()

btn = Button(app, text="Calculate")
btn.pack()

def calculate():
    infix_str = infix.get()
    tempinfix_str = parse_infix(infix_str)
    postfix_str = convert_to_postfix(tempinfix_str)
    result_str = calculate_postfix(postfix_str)
    tempinfix.delete(0, END)
    tempinfix.insert(0, tempinfix_str)
    postfix.delete(0, END)
    postfix.insert(0, postfix_str)
    result.delete(0, END)
    result.insert(0, result_str)

btn["command"] = calculate
root.mainloop()