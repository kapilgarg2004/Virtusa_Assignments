import csv
import os
from datetime import datetime
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


DATA_FILE = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Health", "Entertainment", "Other"]


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_expense(date, category, amount, description):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as f:
        fieldnames = ["date", "category", "amount", "description"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        })


def add_expense():
    print("\nAdding a new expense")
    print("-" * 30)

    date_input = input("Date (leave blank for today, or enter YYYY-MM-DD): ").strip()
    if not date_input:
        date_input = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("That date format does not look right. Please use YYYY-MM-DD.")
            return

    print("Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    cat_choice = input("Pick a category number: ").strip()
    if not cat_choice.isdigit() or not (1 <= int(cat_choice) <= len(CATEGORIES)):
        print("That is not a valid category number.")
        return
    category = CATEGORIES[int(cat_choice) - 1]

    amount_input = input("Amount spent: ").strip()
    try:
        amount = float(amount_input)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid positive number for the amount.")
        return

    description = input("Short description: ").strip()
    if not description:
        description = "No description"

    save_expense(date_input, category, round(amount, 2), description)
    print(f"\nExpense saved: {category} | {amount:.2f} | {date_input}")


def monthly_summary():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    month_input = input("\nEnter month to review (YYYY-MM), or leave blank for current month: ").strip()
    if not month_input:
        month_input = datetime.today().strftime("%Y-%m")

    filtered = [e for e in expenses if e["date"].startswith(month_input)]
    if not filtered:
        print(f"No expenses found for {month_input}.")
        return

    category_totals = defaultdict(float)
    total = 0.0

    for e in filtered:
        try:
            amt = float(e["amount"])
        except ValueError:
            continue
        category_totals[e["category"]] += amt
        total += amt

    print(f"\nSummary for {month_input}")
    print("=" * 35)
    for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        bar = "#" * int((amt / total) * 30)
        print(f"  {cat:<15} {amt:>8.2f}   {bar}")
    print("-" * 35)
    print(f"  {'Total':<15} {total:>8.2f}")

    highest = max(category_totals, key=category_totals.get)
    lowest = min(category_totals, key=category_totals.get)
    print(f"\nHighest spending category : {highest} ({category_totals[highest]:.2f})")
    print(f"Lowest spending category  : {lowest} ({category_totals[lowest]:.2f})")

    suggestions = {
        "Food":          "Consider meal prepping at home to cut down on eating out.",
        "Travel":        "Try using public transport or carpooling where possible.",
        "Bills":         "Review your subscriptions and cancel ones you rarely use.",
        "Shopping":      "Wait 48 hours before non-essential purchases to avoid impulse buys.",
        "Health":        "Check if your employer covers any of these health expenses.",
        "Entertainment": "Look for free or discounted events in your area.",
        "Other":         "Try to categorize these expenses more specifically next month.",
    }

    print("\nSuggestions")
    print("-" * 35)
    found = False
    for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total) * 100
        if pct > 25:
            tip = suggestions.get(cat, "Consider reducing spending here.")
            print(f"  {cat} is {pct:.1f}% of your budget. {tip}")
            found = True
    if not found:
        print("  Your spending looks fairly balanced this month.")


def show_pie_chart():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    if not MATPLOTLIB_AVAILABLE:
        print("\nmatplotlib is not installed. Run: pip install matplotlib")
        return

    month_input = input("\nEnter month for pie chart (YYYY-MM), or leave blank for current month: ").strip()
    if not month_input:
        month_input = datetime.today().strftime("%Y-%m")

    filtered = [e for e in expenses if e["date"].startswith(month_input)]
    if not filtered:
        print(f"No expenses found for {month_input}.")
        return

    category_totals = defaultdict(float)
    for e in filtered:
        try:
            category_totals[e["category"]] += float(e["amount"])
        except ValueError:
            continue

    labels = list(category_totals.keys())
    sizes = list(category_totals.values())
    total = sum(sizes)

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        autopct=lambda p: f"{p:.1f}%" if p > 4 else "",
        startangle=140,
        pctdistance=0.75,
        wedgeprops={"linewidth": 1.2, "edgecolor": "white"}
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    legend_labels = [f"{cat}  -  {amt:.2f} ({amt/total*100:.1f}%)" for cat, amt in zip(labels, sizes)]
    ax.legend(
        wedges,
        legend_labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
        title_fontsize=11
    )
    ax.set_title(f"Spending breakdown for {month_input}", fontsize=13, pad=20)
    plt.tight_layout()
    plt.show()


def view_all():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print(f"\n{'Date':<12} {'Category':<15} {'Amount':>8}  Description")
    print("-" * 60)
    for e in expenses:
        try:
            amt = float(e["amount"])
        except ValueError:
            amt = 0.0
        print(f"{e['date']:<12} {e['category']:<15} {amt:>8.2f}  {e['description']}")

    total = sum(float(e["amount"]) for e in expenses if e["amount"].replace(".", "").isdigit())
    print("-" * 60)
    print(f"{'Total':<28} {total:>8.2f}")


def main():
    print("\nWelcome to your Expense Tracker")
    print("=" * 35)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Add an expense")
        print("  2. Monthly summary")
        print("  3. View all expenses")
        print("  4. Show pie chart")
        print("  5. Exit")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            monthly_summary()
        elif choice == "3":
            view_all()
        elif choice == "4":
            show_pie_chart()
        elif choice == "5":
            print("\nGoodbye. Keep tracking those expenses.\n")
            break
        else:
            print("Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()