"""Tests for database CRUD operations (all data stays in a temporary file)."""

import database
from pathlib import Path


def test_database_create_add_update_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.create_table()
    assert database.get_expenses() == []

    database.add_expense("Coffee", 120, "Food", "2026-11-18", "UPI")
    record = database.get_expenses()[0]
    assert record[1:] == ("Coffee", 120.0, "Food", "2026-11-18", "UPI")

    assert database.update_expense(record[0], "Tea", 80, "Food", "2026-11-18", "Cash")
    assert database.get_expenses()[0][1] == "Tea"
    assert database.delete_expense(record[0])
    assert database.get_expenses() == []
    assert not database.delete_expense(record[0])


def test_database_path_is_anchored_to_source_file():
    assert database.DB_PATH.name == "expenses.db"
    assert database.DB_PATH.parent == Path(database.__file__).resolve().parent
