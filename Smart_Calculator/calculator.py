import tkinter as tk

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def mod(a, b):
    if b == 0:
        return "Error: Modulo by zero"
    return a % b

def lcm(a, b):
    a, b = int(a), int(b)
    if a <= 0 or b <= 0:
        return "Error: Positive numbers required"
    L = a if a > b else b
    while L <= a * b:
        if L % a == 0 and L % b == 0:
            return L
        L += 1
    return a * b

def hcf(a, b):
    a, b = int(a), int(b)
    if a <= 0 or b <= 0:
        return "Error: Positive numbers required"
    H = a if a < b else b
    while H >= 1:
        if a % H == 0 and b % H == 0:
            return H
        H -= 1
    return 1

def extract_from_text(text):
    nums = []
    for t in text.split(' '):
        try:
            nums.append(float(t))
        except ValueError:
            pass
    return nums

operations = {
    'ADD': add, 'ADDITION': add, 'SUM': add, 'PLUS': add,
    'SUB': sub, 'DIFFERENCE': sub, 'MINUS': sub, 'SUBTRACT': sub, 'DIFF': sub,
    'LCM': lcm, 'HCF': hcf, 'PRODUCT': mul, 'MULTIPLICATION': mul,
    'MULTIPLY': mul, 'DIVISION': div, 'DIV': div, 'DIVIDE': div,
    'MOD': mod, 'REMAINDER': mod, 'MODULUS': mod
}

def run_gui():
    win = tk.Tk()
    win.title('Smart Calculator')
    win.geometry('500x300')
    win.configure(bg='lightskyblue')
    win.resizable(False, False)

    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=2)
    win.columnconfigure(2, weight=1)

    l1 = tk.Label(win, text='I am a smart calculator', width=20)
    l1.grid(column=1, row=1, padx=5, pady=10)

    l2 = tk.Label(win, text='My name is Leah', width=20)
    l2.grid(column=1, row=2, padx=5, pady=10)

    l3 = tk.Label(win, text='What can I help you?', width=20)
    l3.grid(column=1, row=3, padx=5, pady=10)

    textin = tk.StringVar()
    e1 = tk.Entry(win, width=30, textvariable=textin)
    e1.grid(column=1, row=4, padx=5, pady=10)
    e1.focus_set()

    res_listbox = tk.Listbox(win, width=40, height=3)
    res_listbox.grid(column=1, row=6, padx=5, pady=10)

    def calculate():
        text = textin.get().strip()
        found = False
        for word in text.split(' '):
            up_word = word.upper()
            if up_word in operations:
                found = True
                try:
                    nums = extract_from_text(text)
                    if len(nums) < 2:
                        res_listbox.delete(0, tk.END)
                        res_listbox.insert(tk.END, "Please enter two numbers in query")
                    else:
                        r = operations[up_word](nums[0], nums[1])
                        res_listbox.delete(0, tk.END)
                        res_listbox.insert(tk.END, r)
                except Exception as err:
                    res_listbox.delete(0, tk.END)
                    res_listbox.insert(tk.END, f"Error: {err}")
                break

        if not found:
            res_listbox.delete(0, tk.END)
            res_listbox.insert(tk.END, 'Operation not recognized. Try: SUM 5 3')

    b1 = tk.Button(win, text='Just this', command=calculate)
    b1.grid(column=1, row=5, padx=5, pady=10)

    win.mainloop()

def main():
    run_gui()

if __name__ == '__main__':
    main()

