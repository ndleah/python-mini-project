import sys
import tkinter as tk
from tkinter import messagebox, ttk

try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    BaseAppClass = ctk.CTk
except Exception:
    BaseAppClass = tk.Tk

class FinanceTrackerCore:
    """Core financial tracking logic separate from GUI."""
    def __init__(self):
        self.income = 0.0
        self.expense = 0.0
        self.income_transactions = []
        self.expense_transactions = []

    def add_income(self, category: str, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.income += amount
        self.income_transactions.append((category, amount))
        return self.income

    def add_expense(self, category: str, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.expense += amount
        self.expense_transactions.append((category, amount))
        return self.expense

    def get_balance(self) -> float:
        return self.income - self.expense

class Application(BaseAppClass):
    def __init__(self):
        super().__init__()

        self.title("Finance Tracker")
        self.geometry("800x500")

        self.core = FinanceTrackerCore()

        if hasattr(ctk, 'CTkFrame'):
            self.grid_columnconfigure(1, weight=5)
            self.grid_rowconfigure(0, weight=5)

            self.main_frame = ctk.CTkFrame(self, corner_radius=0)
            self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

            self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Finance Tracker", font=ctk.CTkFont(size=26, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

            self.income_button = ctk.CTkButton(self.sidebar_frame, text="Income", command=self.income_button_event)
            self.income_button.grid(row=1, column=0, padx=20, pady=15)
            self.expenses_button = ctk.CTkButton(self.sidebar_frame, text="Expenses", command=self.expenses_button_event)
            self.expenses_button.grid(row=2, column=0, padx=20, pady=15)
            self.balance_button = ctk.CTkButton(self.sidebar_frame, text="Balance", command=self.balance_button_event)
            self.balance_button.grid(row=3, column=0, padx=20, pady=15)

            self.income_frame, self.income_tree = self.create_transaction_frame("Income", self.add_income, row=1, transactions=self.core.income_transactions)
            self.expense_frame, self.expense_tree = self.create_transaction_frame("Expense", self.add_expense, row=2, transactions=self.core.expense_transactions)
            self.balance_frame = self.create_balance_frame(row=3)

            self.hide_frames()
            self.income_frame.grid()

            try:
                from matplotlib.figure import Figure
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                self.fig = Figure(figsize=(4, 4), dpi=100)
                self.canvas = FigureCanvasTkAgg(self.fig, master=self.balance_frame)
                self.canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20)
            except Exception:
                self.fig = None
                self.canvas = None

    def create_transaction_frame(self, title, button_command, row, transactions):
        frame = ctk.CTkFrame(self.main_frame)
        ctk.CTkLabel(frame, text=f"Add {title}", font=ctk.CTkFont(size=20)).grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(frame, text="Category").grid(row=1, column=0, padx=10, pady=5)
        category_entry = ctk.CTkEntry(frame)
        category_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame, text="Amount").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = ctk.CTkEntry(frame)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(frame, text=f"Add {title}", command=lambda: button_command(category_entry, amount_entry)).grid(row=3, column=0, columnspan=2, pady=10)

        tree = ttk.Treeview(frame)
        tree["columns"] = ("Category", "Amount")
        tree.column("#0", width=0, stretch="NO")
        tree.column("Category", anchor="w", width=120)
        tree.column("Amount", anchor="w", width=120)
        tree.heading("Category", text="Category", anchor='w')
        tree.heading("Amount", text="Amount", anchor='w')
        tree.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

        return frame, tree

    def create_balance_frame(self, row):
        frame = ctk.CTkFrame(self.main_frame)
        self.balance_label = ctk.CTkLabel(frame, text="Current Net Balance: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.balance_label.grid(row=0, column=0, padx=20, pady=10)
        return frame

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
        self.balance_label.configure(text=f"Current Net Balance: ${self.core.get_balance():.2f}")
        self.update_plot()

    def add_income(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get().strip() or "General"
        if amount is not None:
            self.core.add_income(category, amount)
            self.update_table(self.income_tree, self.core.income_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def add_expense(self, category_entry, amount_entry):
        amount = self.get_amount_from_entry(amount_entry)
        category = category_entry.get().strip() or "General"
        if amount is not None:
            self.core.add_expense(category, amount)
            self.update_table(self.expense_tree, self.core.expense_transactions)
            category_entry.delete(0, 'end')
            amount_entry.delete(0, 'end')

    def get_amount_from_entry(self, entry):
        try:
            amount = float(entry.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive numeric amount.")
            return None

    def update_plot(self):
        if not hasattr(self, 'fig') or self.fig is None:
            return
        self.fig.clear()
        ax = self.fig.add_subplot(111)

        if self.core.income == 0 and self.core.expense == 0:
            ax.text(0.5, 0.5, 'No Transactions Logged Yet', horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax.axis('off')
        else:
            ax.pie([self.core.income, self.core.expense], labels=['Income', 'Expense'], autopct='%1.1f%%', colors=['#2ECC71', '#E74C3C'])
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.draw()

    def update_table(self, tree, transactions):
        for i in tree.get_children():
            tree.delete(i)
        for transaction in transactions:
            tree.insert('', 'end', values=transaction)

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()