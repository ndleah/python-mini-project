import json
import os
from datetime import datetime
from collections import defaultdict


class ExpenseTracker:
    DATA_FILE = "expenses_data.json"

    def __init__(self):
        self.expenses = {}
        self.categories = {}
        self.load_data()


    def save_data(self):
        """Save expenses and categories to a JSON file."""
        data = {
            "expenses": self.expenses,
            "categories": self.categories
        }
        try:
            with open(self.DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"⚠️  Error saving data: {e}")

    def load_data(self):
        """Load expenses and categories from a JSON file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.expenses = data.get("expenses", {})
                    self.categories = data.get("categories", {})
                    print("✅ Data loaded successfully!")
            except (IOError, json.JSONDecodeError) as e:
                print(f"⚠️  Error loading data: {e}. Starting fresh.")
                self.expenses = {}
                self.categories = {}

    # ──────────────────────────── Core Operations ─────────────────────────────

    def add_expense(self, date, amount, category, description=""):
        """Add an expense entry with validation."""
        if category not in self.categories:
            print(f"⚠️  Category '{category}' doesn't exist. Creating it automatically.")
            self.add_category(category)

        if category not in self.expenses:
            self.expenses[category] = []

        self.expenses[category].append({
            "date": date,
            "amount": amount,
            "description": description
        })

        budget_limit = self.categories.get(category, 0)
        if budget_limit > 0:
            total_spent = sum(item["amount"] for item in self.expenses[category])
            percentage = (total_spent / budget_limit) * 100
            if total_spent > budget_limit:
                print(f"🚨 BUDGET EXCEEDED for '{category}'! "
                      f"Spent: ${total_spent:.2f} / Budget: ${budget_limit:.2f} "
                      f"({percentage:.1f}%)")
            elif percentage >= 80:
                print(f"⚠️  Warning: You've used {percentage:.1f}% of your "
                      f"'{category}' budget (${total_spent:.2f}/${budget_limit:.2f})")

        self.save_data()
        print(f"✅ Expense of ${amount:.2f} added to '{category}'.")

    def add_category(self, category, budget_limit=0):
        """Add a new category with an optional budget limit."""
        if category in self.categories:
            print(f"⚠️  Category '{category}' already exists.")
            return False
        self.categories[category] = budget_limit
        self.save_data()
        print(f"✅ Category '{category}' added"
              f"{f' with budget ${budget_limit:.2f}' if budget_limit > 0 else ''}.")
        return True

    def delete_expense(self, category, index):
        """Delete a specific expense by category and index."""
        if category not in self.expenses or not self.expenses[category]:
            print(f"⚠️  No expenses found in '{category}'.")
            return False

        if 0 <= index < len(self.expenses[category]):
            removed = self.expenses[category].pop(index)
            if not self.expenses[category]:
                del self.expenses[category]
            self.save_data()
            print(f"✅ Removed expense: ${removed['amount']:.2f} on {removed['date']}")
            return True
        else:
            print("⚠️  Invalid expense index.")
            return False

    def delete_category(self, category):
        """Delete a category and all its expenses."""
        if category not in self.categories:
            print(f"⚠️  Category '{category}' not found.")
            return False
        del self.categories[category]
        if category in self.expenses:
            del self.expenses[category]
        self.save_data()
        print(f"✅ Category '{category}' and its expenses deleted.")
        return True

    def edit_expense(self, category, index, new_date=None, new_amount=None,
                     new_description=None):
        """Edit an existing expense."""
        if category not in self.expenses or index >= len(self.expenses[category]):
            print("⚠️  Invalid category or index.")
            return False

        expense = self.expenses[category][index]
        if new_date:
            expense["date"] = new_date
        if new_amount is not None:
            expense["amount"] = new_amount
        if new_description is not None:
            expense["description"] = new_description

        self.save_data()
        print("✅ Expense updated successfully.")
        return True

    def view_expenses(self, category_filter=None):
        """View all expenses, optionally filtered by category."""
        if not self.expenses:
            print("📭 No expenses recorded yet.")
            return

        grand_total = 0
        print("\n" + "=" * 65)
        print(f"{'EXPENSE REPORT':^65}")
        print("=" * 65)

        categories_to_show = ({category_filter: self.expenses.get(category_filter, [])}
                              if category_filter and category_filter in self.expenses
                              else self.expenses)

        for category, items in categories_to_show.items():
            if not items:
                continue
            budget = self.categories.get(category, 0)
            total = sum(item["amount"] for item in items)
            grand_total += total

            budget_str = f" (Budget: ${budget:.2f})" if budget > 0 else ""
            print(f"\n📁 {category}{budget_str}")
            print("-" * 60)
            print(f"  {'#':<4} {'Date':<14} {'Amount':>10}  {'Description'}")
            print(f"  {'─'*3}  {'─'*12}  {'─'*10}  {'─'*25}")

            for i, item in enumerate(items):
                desc = item.get("description", "N/A") or "N/A"
                print(f"  {i+1:<4} {item['date']:<14} ${item['amount']:>9.2f}  {desc}")

            print(f"  {'':>18} {'─'*10}")
            print(f"  {'Subtotal:':>18} ${total:>9.2f}")

            if budget > 0:
                remaining = budget - total
                status = "✅" if remaining >= 0 else "🚨"
                print(f"  {'Remaining:':>18} ${remaining:>9.2f} {status}")

        print("\n" + "=" * 65)
        print(f"  {'GRAND TOTAL:':>18} ${grand_total:>9.2f}")
        print("=" * 65)

    def view_categories(self):
        """View all categories with their budgets and spending."""
        if not self.categories:
            print("📭 No categories created yet.")
            return

        print("\n" + "=" * 55)
        print(f"{'CATEGORIES OVERVIEW':^55}")
        print("=" * 55)
        print(f"  {'Category':<20} {'Budget':>10} {'Spent':>10} {'Status':>10}")
        print(f"  {'─'*18}  {'─'*10} {'─'*10} {'─'*10}")

        for category, budget in self.categories.items():
            items = self.expenses.get(category, [])
            spent = sum(item["amount"] for item in items)
            budget_str = f"${budget:.2f}" if budget > 0 else "No limit"

            if budget > 0:
                percentage = (spent / budget) * 100
                if percentage > 100:
                    status = f"🚨 {percentage:.0f}%"
                elif percentage >= 80:
                    status = f"⚠️ {percentage:.0f}%"
                else:
                    status = f"✅ {percentage:.0f}%"
            else:
                status = "—"

            print(f"  {category:<20} {budget_str:>10} ${spent:>9.2f} {status:>10}")
        print("=" * 55)

    def view_expenses_by_date(self, start_date=None, end_date=None):
        """View expenses filtered by date range."""
        all_expenses = []
        for category, items in self.expenses.items():
            for item in items:
                all_expenses.append({**item, "category": category})

        if start_date:
            all_expenses = [e for e in all_expenses if e["date"] >= start_date]
        if end_date:
            all_expenses = [e for e in all_expenses if e["date"] <= end_date]

        all_expenses.sort(key=lambda x: x["date"])

        if not all_expenses:
            print("📭 No expenses found for the given date range.")
            return

        total = sum(e["amount"] for e in all_expenses)
        date_range = ""
        if start_date and end_date:
            date_range = f" ({start_date} to {end_date})"
        elif start_date:
            date_range = f" (from {start_date})"
        elif end_date:
            date_range = f" (until {end_date})"

        print(f"\n{'EXPENSES BY DATE' + date_range:^65}")
        print("=" * 65)
        print(f"  {'Date':<14} {'Category':<18} {'Amount':>10}  {'Description'}")
        print(f"  {'─'*12}  {'─'*16}  {'─'*10}  {'─'*20}")

        for e in all_expenses:
            desc = e.get("description", "N/A") or "N/A"
            print(f"  {e['date']:<14} {e['category']:<18} ${e['amount']:>9.2f}  {desc}")

        print(f"\n  {'Total:':>34} ${total:>9.2f}")
        print("=" * 65)

    def get_monthly_summary(self):
        """Generate a monthly spending summary."""
        monthly = defaultdict(lambda: defaultdict(float))

        for category, items in self.expenses.items():
            for item in items:
                try:
                    month_key = item["date"][:7]
                    monthly[month_key][category] += item["amount"]
                except (KeyError, IndexError):
                    continue

        if not monthly:
            print("📭 No expenses to summarize.")
            return

        print(f"\n{'MONTHLY SUMMARY':^65}")
        print("=" * 65)

        for month in sorted(monthly.keys()):
            try:
                month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
            except ValueError:
                month_name = month

            month_total = sum(monthly[month].values())
            print(f"\n📅 {month_name} — Total: ${month_total:.2f}")
            print("-" * 50)

            for cat, amount in sorted(monthly[month].items(),
                                      key=lambda x: x[1], reverse=True):
                bar_length = int((amount / month_total) * 30) if month_total else 0
                bar = "█" * bar_length
                percentage = (amount / month_total) * 100 if month_total else 0
                print(f"  {cat:<18} ${amount:>9.2f} ({percentage:>5.1f}%) {bar}")

        print("=" * 65)

    def search_expenses(self, keyword):
        """Search expenses by description keyword."""
        results = []
        keyword_lower = keyword.lower()

        for category, items in self.expenses.items():
            for i, item in enumerate(items):
                desc = item.get("description", "").lower()
                if keyword_lower in desc or keyword_lower in category.lower():
                    results.append({**item, "category": category, "index": i})

        if not results:
            print(f"🔍 No expenses found matching '{keyword}'.")
            return

        print(f"\n🔍 Search Results for '{keyword}' ({len(results)} found):")
        print("-" * 60)
        for r in results:
            desc = r.get("description", "N/A") or "N/A"
            print(f"  [{r['category']}] {r['date']} — ${r['amount']:.2f} — {desc}")

    def export_to_csv(self, filename="expenses_export.csv"):
        """Export all expenses to a CSV file."""
        try:
            import csv
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Category", "Amount", "Description"])
                for category, items in self.expenses.items():
                    for item in items:
                        writer.writerow([
                            item["date"],
                            category,
                            f"{item['amount']:.2f}",
                            item.get("description", "")
                        ])
            print(f"✅ Expenses exported to '{filename}'.")
        except IOError as e:
            print(f"⚠️  Error exporting: {e}")


def validate_date(date_str):
    """Validate and return a date string in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_amount(amount_str):
    """Validate and return a positive float amount."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            print("⚠️  Amount must be positive.")
            return None
        return amount
    except ValueError:
        print("⚠️  Invalid amount. Please enter a number.")
        return None


def get_valid_date(prompt="Enter date (YYYY-MM-DD) [or press Enter for today]: "):
    """Get a validated date from user input."""
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        if validate_date(date_str):
            return date_str
        print("⚠️  Invalid date format. Please use YYYY-MM-DD.")


def get_valid_amount(prompt="Enter amount: $"):
    """Get a validated amount from user input."""
    while True:
        amount = validate_amount(input(prompt).strip())
        if amount is not None:
            return amount


def display_menu():
    """Display the main menu."""
    print("\n" + "╔" + "═" * 40 + "╗")
    print("║" + " 💰 EXPENSE TRACKER ".center(40) + "║")
    print("╠" + "═" * 40 + "╣")
    print("║  1.  ➕ Add Expense                    ║")
    print("║  2.  📁 Add Category                   ║")
    print("║  3.  📊 View Expenses                  ║")
    print("║  4.  📂 View Categories                ║")
    print("║  5.  📅 View by Date Range             ║")
    print("║  6.  📈 Monthly Summary                ║")
    print("║  7.  🔍 Search Expenses                ║")
    print("║  8.  ✏️  Edit Expense                   ║")
    print("║  9.  🗑️  Delete Expense                 ║")
    print("║  10. 🗑️  Delete Category                ║")
    print("║  11. 📤 Export to CSV                   ║")
    print("║  12. 🚪 Exit                           ║")
    print("╚" + "═" * 40 + "╝")


def main():
    tracker = ExpenseTracker()

    while True:
        display_menu()
        choice = input("\n  Enter your choice (1-12): ").strip()

        if choice == "1":
            print("\n--- Add New Expense ---")
            date = get_valid_date()
            amount = get_valid_amount()
            category = input("Enter category: ").strip()
            if not category:
                print("⚠️  Category cannot be empty.")
                continue
            description = input("Enter description (optional): ").strip()
            tracker.add_expense(date, amount, category, description)

        elif choice == "2":
            print("\n--- Add New Category ---")
            category = input("Enter category name: ").strip()
            if not category:
                print("⚠️  Category name cannot be empty.")
                continue
            budget_input = input("Enter budget limit (or press Enter for no limit): $").strip()
            budget = 0
            if budget_input:
                budget = validate_amount(budget_input)
                if budget is None:
                    budget = 0
            tracker.add_category(category, budget)

        elif choice == "3":
            print("\n--- View Expenses ---")
            filter_choice = input("Filter by category? (Enter category name or press Enter for all): ").strip()
            if filter_choice:
                tracker.view_expenses(category_filter=filter_choice)
            else:
                tracker.view_expenses()

        elif choice == "4":
            tracker.view_categories()

        elif choice == "5":
            print("\n--- View by Date Range ---")
            start = input("Start date (YYYY-MM-DD, or Enter to skip): ").strip()
            end = input("End date (YYYY-MM-DD, or Enter to skip): ").strip()

            if start and not validate_date(start):
                print("⚠️  Invalid start date.")
                continue
            if end and not validate_date(end):
                print("⚠️  Invalid end date.")
                continue

            tracker.view_expenses_by_date(
                start_date=start if start else None,
                end_date=end if end else None
            )

        elif choice == "6":
            tracker.get_monthly_summary()

        elif choice == "7":
            keyword = input("Enter search keyword: ").strip()
            if keyword:
                tracker.search_expenses(keyword)
            else:
                print("⚠️  Please enter a keyword to search.")

        elif choice == "8":
            print("\n--- Edit Expense ---")
            tracker.view_expenses()
            category = input("Enter category of expense to edit: ").strip()
            if category not in tracker.expenses:
                print("⚠️  Category not found.")
                continue
            try:
                index = int(input("Enter expense number to edit: ")) - 1
            except ValueError:
                print("⚠️  Invalid number.")
                continue

            print("Press Enter to keep current value.")
            new_date = input("New date (YYYY-MM-DD): ").strip()
            if new_date and not validate_date(new_date):
                print("⚠️  Invalid date.")
                continue

            new_amount_str = input("New amount: $").strip()
            new_amount = None
            if new_amount_str:
                new_amount = validate_amount(new_amount_str)
                if new_amount is None:
                    continue

            new_desc = input("New description: ").strip()

            tracker.edit_expense(
                category, index,
                new_date=new_date if new_date else None,
                new_amount=new_amount,
                new_description=new_desc if new_desc else None
            )

        elif choice == "9":
            print("\n--- Delete Expense ---")
            tracker.view_expenses()
            category = input("Enter category: ").strip()
            if category not in tracker.expenses:
                print("⚠️  Category not found.")
                continue
            try:
                index = int(input("Enter expense number to delete: ")) - 1
            except ValueError:
                print("⚠️  Invalid number.")
                continue
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                tracker.delete_expense(category, index)

        elif choice == "10":
            print("\n--- Delete Category ---")
            tracker.view_categories()
            category = input("Enter category to delete: ").strip()
            confirm = input(f"Delete '{category}' and ALL its expenses? (y/n): ").strip().lower()
            if confirm == 'y':
                tracker.delete_category(category)

        elif choice == "11":
            filename = input("Enter filename (or Enter for 'expenses_export.csv'): ").strip()
            tracker.export_to_csv(filename if filename else "expenses_export.csv")

        elif choice == "12":
            tracker.save_data()
            print("\n👋 Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("⚠️  Invalid choice. Please enter a number between 1-12.")


if __name__ == "__main__":
    main()