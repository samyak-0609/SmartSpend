"""Validation and business rules for expenses."""

from datetime import date as date_type

from database import (
    add_expense as db_add_expense,
    delete_expense as db_delete_expense,
    get_expenses,
    update_expense as db_update_expense,
)


def _validate(title: str, amount: float, date: str) -> None:
    if not title or not title.strip():
        raise ValueError("Expense title cannot be empty.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    try:
        date_type.fromisoformat(date)
    except (TypeError, ValueError) as exc:
        raise ValueError("Date must be a valid date in YYYY-MM-DD format.") from exc


def add_new_expense(title, amount, category, date, payment_method):
    _validate(title, amount, date)
    db_add_expense(title, amount, category, date, payment_method)
    return "Expense added successfully."


def view_expenses():
    return get_expenses()


def remove_expense(expense_id):
    if not db_delete_expense(int(expense_id)):
        raise ValueError("That expense no longer exists.")
    return "Expense deleted successfully."


def edit_expense(expense_id, title, amount, category, date, payment_method):
    _validate(title, amount, date)
    if not db_update_expense(int(expense_id), title, amount, category, date, payment_method):
        raise ValueError("That expense no longer exists.")
    return "Expense updated successfully."
