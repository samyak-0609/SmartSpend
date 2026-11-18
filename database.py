"""SQLite persistence for SmartSpend."""

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().with_name("expenses.db")


def connect_db() -> sqlite3.Connection:
    """Open the project's database, independent of the launch directory."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def create_table() -> None:
    with closing(connect_db()) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                payment_method TEXT NOT NULL
            )"""
        )
        conn.commit()


def add_expense(title: str, amount: float, category: str, date: str,
                payment_method: str) -> None:
    with closing(connect_db()) as conn:
        conn.execute(
            "INSERT INTO expenses (title, amount, category, date, payment_method) "
            "VALUES (?, ?, ?, ?, ?)",
            (title.strip(), float(amount), category, date, payment_method),
        )
        conn.commit()


def get_expenses() -> list[tuple[Any, ...]]:
    with closing(connect_db()) as conn:
        rows = conn.execute(
            "SELECT id, title, amount, category, date, payment_method "
            "FROM expenses ORDER BY date DESC, id DESC"
        ).fetchall()
    return [tuple(row) for row in rows]


def delete_expense(expense_id: int) -> bool:
    with closing(connect_db()) as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
    return cursor.rowcount > 0


def update_expense(expense_id: int, title: str, amount: float, category: str,
                   date: str, payment_method: str) -> bool:
    with closing(connect_db()) as conn:
        cursor = conn.execute(
            """UPDATE expenses
               SET title = ?, amount = ?, category = ?, date = ?, payment_method = ?
               WHERE id = ?""",
            (title.strip(), float(amount), category, date, payment_method, expense_id),
        )
        conn.commit()
    return cursor.rowcount > 0
