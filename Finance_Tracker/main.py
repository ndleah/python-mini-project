import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")

        self.income = 0
        self.expense = 0

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

    
    def add_income(self):
        try:
            amount = float(self.income_entry.get())
            self.income += amount
            self.update_plot()
            self.income_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for income")


    def add_expense(self):
        try:
            amount = float(self.expense_entry.get())
            self.expense += amount
            self.update_plot()
            self.expense_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for expense")

    def update_plot(self):
        self.fig.clear()
        plt.figure(self.fig.number)
        plt.pie([self.income, self.expense], labels=['Income', 'Expense'], autopct='%1.1f%%')
        self.canvas.draw()
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()

