import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")

        self.income = 0
        self.expense = 0
        self.transactions = []  # Add this line to initialize the transactions list

        # Income Entry
        tk.Label(self, text="Income: ").grid(row=0, column=0)
        self.income_entry = tk.Entry(self)
        self.income_entry.grid(row=0, column=1)

        # Expense Entry
        tk.Label(self, text="Expense: ").grid(row=1, column=0)
        self.expense_entry = tk.Entry(self)
        self.expense_entry.grid(row=1, column=1)

        # Buttons
        tk.Button(self, text="Add Income", command=self.add_income).grid(row=2, column=0)
        tk.Button(self, text="Add Expense", command=self.add_expense).grid(row=2, column=1)

        # Plot
        self.fig = Figure(figsize = (5, 5), dpi = 100) 
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

        # Table (Treeview)
        self.tree = ttk.Treeview(self, columns=('Transaction', 'Amount'), show='headings')
        self.tree.heading('Transaction', text='Transaction')
        self.tree.heading('Amount', text='Amount')
        self.tree.grid(row=4, column=0, columnspan=2)

    
    def add_income(self):
        try:
            amount = float(self.income_entry.get())
            if amount <= 0:
                raise ValueError
            self.income += amount
            self.transactions.append(('Income', amount))
            self.update_table()
            self.update_plot()
            self.income_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number for income")


    def add_expense(self):
        try:
            amount = float(self.expense_entry.get())
            if amount <= 0:
                raise ValueError
            self.expense += amount
            self.transactions.append(('Expense', amount))
            self.update_table()
            self.update_plot()
            self.expense_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number for expense")


    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)  # Creates a new subplot
        ax.pie([self.income, self.expense], labels=['Income', 'Expense'], autopct='%1.1f%%')
        self.canvas.draw()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for transaction in self.transactions:
            self.tree.insert('', 'end', values=transaction)
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()
