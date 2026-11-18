"""Tests for expense business rules using an isolated temporary database."""

import pytest

import database
from expense import add_new_expense, edit_expense, remove_expense, view_expenses


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "expenses.db")
    database.create_table()


def test_add_edit_view_and_remove_expense():
    message = add_new_expense(" Lunch ", 150, "Food", "2026-11-18", "Cash")
    assert message == "Expense added successfully."
    expense_id = view_expenses()[0][0]

    edit_expense(expense_id, "Dinner", 200, "Food", "2026-11-18", "UPI")
    updated = view_expenses()[0]
    assert updated[1:3] == ("Dinner", 200.0)
    assert updated[5] == "UPI"

    remove_expense(expense_id)
    assert view_expenses() == []


@pytest.mark.parametrize(
    ("title", "amount", "date"),
    [("  ", 100, "2026-11-18"), ("Bus", 0, "2026-11-18"),
     ("Bus", -1, "2026-11-18"), ("Bus", 100, "not-a-date")],
)
def test_invalid_expense_is_rejected(title, amount, date):
    with pytest.raises(ValueError):
        add_new_expense(title, amount, "Travel", date, "Cash")


def test_edit_or_delete_missing_expense_is_reported():
    with pytest.raises(ValueError, match="no longer exists"):
        edit_expense(404, "Bus", 100, "Travel", "2026-11-18", "Cash")
    with pytest.raises(ValueError, match="no longer exists"):
        remove_expense(404)
