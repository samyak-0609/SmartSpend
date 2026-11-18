"""Reusable spending summaries for SmartSpend."""

import pandas as pd


def category_totals(expenses: pd.DataFrame) -> pd.Series:
    """Return total spending per category, highest first."""
    if expenses.empty:
        return pd.Series(dtype="float64", name="Amount")
    return expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).rename("Amount")


def monthly_totals(expenses: pd.DataFrame) -> pd.Series:
    """Return monthly spending totals in chronological order."""
    if expenses.empty:
        return pd.Series(dtype="float64", name="Amount")
    dates = pd.to_datetime(expenses["Date"], errors="coerce")
    amounts = pd.to_numeric(expenses["Amount"], errors="coerce").fillna(0)
    frame = pd.DataFrame({"Month": dates.dt.to_period("M").astype(str), "Amount": amounts})
    return frame.dropna(subset=["Month"]).groupby("Month")["Amount"].sum().sort_index()


def spending_summary(expenses: pd.DataFrame) -> dict[str, float | int]:
    """Summarize transaction count, total, and average spending."""
    if expenses.empty:
        return {"count": 0, "total": 0.0, "average": 0.0}
    amounts = pd.to_numeric(expenses["Amount"], errors="coerce").fillna(0)
    return {"count": int(len(amounts)), "total": float(amounts.sum()),
            "average": float(amounts.mean())}
