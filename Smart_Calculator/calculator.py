from tkinter import *

def add(a,b):
    return a + b

def sub(a,b):
    return a - b

def mul(a,b):
    return a * b

def div(a,b):
    return a / b

def mod(a,b):
    return a % b

def lcm(a,b):
    if a<0 or b<0: return
    L = a if a > b else b
    while L <= a * b:
        if L%a == 0 and L%b ==0:
            return L
        L+=1

def hcf(a,b):
    if a<0 or b<0: return
    H = a if a<b else b
    while H >= 1:
        if a%H == 0 and b%H ==0:
            return H
        H-=1

def extract_from_text(text):
    l = []
    for t in text.split(' '):
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

def calculate():
    text = textin.get()
    for word in text.split(' '):
        if word.upper() in operations.keys():
            try:
                l = extract_from_text(text)
                r = operations[word.upper()](l[0], l[1])
                list.delete(0,END)
                list.insert(END,r)
            except:
                list.delete(0,END)
                list.insert(END,'something went wrong please enter again')
            finally:
                break
        elif word.upper() not in operations.keys():
            list.delete(0,END)
            list.insert(END,'something went wrong please enter again')

operations = {'ADD':add,'ADDITION':add, 'SUM':add, 'PLUS':add,
            'SUB':sub, 'DIFFERENCE':sub, 'MINUS': sub, 'SUBTRACT':sub, 'DIFF':sub,
            'LCM':lcm, 'HCF':hcf, 'PRODUCT':mul, 'MULTIPLICATION':mul,
            'MULTIPLY':mul, 'DIVISION':div, 'DIV':div, 'DIVIDE':div,
            'MOD':mod,'REMAINDER':mod, 'MODULUS':mod}


win = Tk()
win.title('Smart Calculator')
win.geometry('500x300')
win.configure(bg='lightskyblue')

win.resizable(0, 0)
win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=2)
win.columnconfigure(2, weight=1)

l1 = Label(win, text='I am a smart calculator', width=20)
l1.grid(column=1, row=1, padx=5, pady=10)

l2 = Label(win, text='My name is Leah', width=20)
l2.grid(column=1, row=2, padx=5, pady=10)

l3 = Label(win, text='What can I help you?', width=20)
l3.grid(column=1, row=3, padx=5, pady=10)

textin = StringVar()
e1 = Entry(win, width=30, textvariable=textin)
e1.grid(column=1, row=4, padx=5, pady=10)

b1 = Button(win, text='Just this', command=calculate)
b1.grid(column=1, row=5, padx=5, pady=10)

list = Listbox(win, width=40, height=3)
list.grid(column=1, row=6, padx=5, pady=10)

win.mainloop()
