import sys

class ExpenseTracker:
    def __init__(self):
        self.expenses = {}
        self.categories = set()

    def add_expense(self, date: str, amount: float, category: str):
        category = category.strip().capitalize() or "General"
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        if category not in self.expenses:
            self.expenses[category] = []
        self.expenses[category].append((date, amount))
        self.categories.add(category)

    def add_category(self, category: str):
        category = category.strip().capitalize()
        if category:
            self.categories.add(category)
            print(f"Category '{category}' added successfully.")

    def view_expenses(self):
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        print("\n=== Expenses Summary by Category ===")
        grand_total = 0.0
        for category, items in self.expenses.items():
            total_amount = sum(amount for _, amount in items)
            grand_total += total_amount
            print(f"  • {category}: ${total_amount:.2f} ({len(items)} transaction(s))")
        print(f"Grand Total: ${grand_total:.2f}")

    def view_categories(self):
        all_cats = sorted(list(self.categories.union(set(self.expenses.keys()))))
        if not all_cats:
            print("\nNo categories registered yet.")
            return
        print("\n=== Categories List ===")
        for cat in all_cats:
            count = len(self.expenses.get(cat, []))
            print(f"  - {cat} ({count} items)")

def run_menu():
    tracker = ExpenseTracker()

    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. Add Category")
        print("3. View Expenses")
        print("4. View Categories")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            while True:
                try:
                    raw_amt = input("Enter amount ($): ").strip()
                    amount = float(raw_amt)
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid amount! Please enter a valid number.")

            category = input("Enter category: ").strip()
            tracker.add_expense(date, amount, category)
            print("Expense recorded successfully!")
        elif choice == "2":
            category = input("Enter new category name: ").strip()
            tracker.add_category(category)
        elif choice == "3":
            tracker.view_expenses()
        elif choice == "4":
            tracker.view_categories()
        elif choice == "5":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def main():
    run_menu()

if __name__ == '__main__':
    main()

