import datetime

class Budget:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.categories = {}
        self.reminders = []

    def add_income(self, amount, category="income"):
        """Add income to the budget."""
        if amount < 0:
            raise ValueError("Income amount cannot be negative.")
        self.income += amount
        self.categories.setdefault(category, {'income': 0, 'expenses': 0, 'budget': 0})
        self.categories[category]['income'] += amount

    def add_expense(self, amount, category="miscellaneous"):
        """Add expenses to the budget."""
        if amount < 0:
            raise ValueError("Expense amount cannot be negative.")
            
        if category not in self.categories:
            raise ValueError("Invalid category. Please set a budget for this category first.")
        
        if self.categories[category]['budget'] < self.categories[category]['expenses'] + amount:
            raise ValueError("Overspending! You cannot spend more than your budget.")
    
        self.expenses += amount
        self.categories[category]['expenses'] += amount

    def set_budget(self, category, budget):
        """Set budget for a specific category."""
        if budget < 0:
            raise ValueError("Budget amount cannot be negative.")
        self.categories.setdefault(category, {'income': 0, 'expenses': 0, 'budget': 0})
        self.categories[category]['budget'] = budget

    def add_reminder(self, date, message):
        """Add a reminder for a specific date."""
        self.reminders.append({'date': date, 'message': message})

    def check_reminders(self):
        """Check and display reminders for the current date."""
        current_date = datetime.datetime.now().date()
        for reminder in self.reminders:
            if reminder['date'] == current_date:
                print(reminder['message'])

    def get_summary(self):
        """Get budget summary."""
        return {
            'income': self.income,
            'expenses': self.expenses,
            'categories': self.categories,
            'remaining_budget': sum(category['budget'] - category['expenses'] for category in self.categories.values())
        }

# Example usage:
budget = Budget()
budget.add_income(1000, "salary")
budget.set_budget("groceries", 800)
budget.add_expense(500, "groceries")
budget.check_reminders()

# Print budget summary
summary = budget.get_summary()
print("Income:", summary['income'])
print("Expenses:", summary['expenses'])
print("Remaining Budget:", summary['remaining_budget'])
print("Category Budgets:", summary['categories'])