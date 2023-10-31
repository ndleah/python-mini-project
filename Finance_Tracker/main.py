import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Finance Tracker")
        self.geometry(f"{800}x{500}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=5)

        self.income = 0
        self.expense = 0
        self.income_transactions = [] 
        self.expense_transactions = []

        # create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Finance Tracker", 
                                                 font=ctk.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Adding navigation buttons
        self.income_button = ctk.CTkButton(self.sidebar_frame, text="Income", command=self.income_button_event)
        self.income_button.grid(row=1, column=0, padx=20, pady=20)
        self.expenses_button = ctk.CTkButton(self.sidebar_frame, text="Expenses", command=self.expenses_button_event)
        self.expenses_button.grid(row=2, column=0, padx=20, pady=20)
        self.balance_button = ctk.CTkButton(self.sidebar_frame, text="Balance", command=self.balance_button_event)
        self.balance_button.grid(row=3, column=0, padx=20, pady=20)

        # Create Entry fields(User can type the text)
        self.income_frame, self.income_tree = self.create_transaction_frame("Income", self.add_income, row=1, transactions=self.income_transactions)
        self.expense_frame, self.expense_tree = self.create_transaction_frame("Expense", self.add_expense, row=2, transactions=self.expense_transactions)
        self.balance_frame = self.create_balance_frame(row=3)

        self.hide_frames()
        self.income_frame.grid()

        # Plot
        self.fig = Figure(figsize = (4, 4), dpi = 100) 
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.balance_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0)

    def create_transaction_frame(self, title, button_command, row, transactions):
        frame = ctk.CTkFrame(self.main_frame)
        ctk.CTkLabel(frame, text=f"Add {title}", font=ctk.CTkFont(size=20)).grid(row=0, column=0)
        
        ctk.CTkLabel(frame, text="Category").grid(row=1, column=0)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1)

        ctk.CTkLabel(frame, text="Amount").grid(row=2, column=0)
        amount_entry = ctk.CTkEntry(frame)
        amount_entry.grid(row=2, column=1)

        ctk.CTkButton(frame, text=f"Add {title}", command=lambda: button_command(category_entry, amount_entry)).grid(row=3, column=0)
        
        # Add a transactions table
        tree = ttk.Treeview(frame)
        tree["columns"]=("Category","Amount")
        tree.column("#0", width=0, stretch="NO")
        tree.column("Category", anchor="w", width=120)
        tree.column("Amount", anchor="w", width=120)
        tree.heading("Category", text="Category",anchor='w')
        tree.heading("Amount", text="Amount",anchor='w')
        tree.grid(row=4, column=0, padx=20, pady=50)
        
        return frame, tree

    def create_balance_frame(self, row):
        frame = ctk.CTkFrame(self.main_frame)
        # create and add your balance widgets here
        return frame

    #Clear the current view of the app
    def hide_frames(self):
        for frame in [self.income_frame, self.expense_frame, self.balance_frame]:
            frame.grid_remove()

    def income_button_event(self):
        self.hide_frames()
        self.income_frame.grid()

    def expenses_button_event(self):
        self.hide_frames()
        self.expense_frame.grid()

    def balance_button_event(self):
        self.hide_frames()
        self.balance_frame.grid()
        self.update_plot()

    def add_income(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.income += amount
            self.income_transactions.append((category, amount))
            self.update_table(self.income_tree, self.income_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def add_expense(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get()
        if amount is not None:
            self.expense += amount
            self.expense_transactions.append((category, amount))
            self.update_table(self.expense_tree, self.expense_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def get_amount_from_entry(self, entry):
        try:
            amount = float(entry.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number")
            return None

    def update_plot(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)  # Creates a new subplot
        ax.pie([self.income, self.expense], labels=['Income', 'Expense'], autopct='%1.1f%%')
        self.canvas.draw()

    def update_table(self, tree, transactions):
        for i in tree.get_children():
            tree.delete(i)
        for transaction in transactions:
            tree.insert('', 'end', values=transaction)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

###########################

#Contributor: Hina Ota

##########################