"""SmartSpend: a local personal expense tracker."""

from datetime import date

import pandas as pd
import streamlit as st

from database import create_table
from expense import add_new_expense, edit_expense, remove_expense, view_expenses
from analytics import category_totals, monthly_totals, spending_summary

st.set_page_config(page_title="SmartSpend", page_icon=":material/account_balance_wallet:", layout="wide")
create_table()

CATEGORIES = ["Food", "Travel", "Shopping", "Education", "Entertainment", "Bills", "Health", "Other"]
PAYMENT_METHODS = ["Cash", "UPI", "Credit Card", "Debit Card"]
COLUMNS = ["ID", "Title", "Amount", "Category", "Date", "Payment Method"]

st.sidebar.title(":material/account_balance_wallet: SmartSpend")
st.sidebar.caption("Personal expense tracker")
page = st.sidebar.radio("Go to", ["Dashboard", "Add expense", "Transactions"],
                        format_func=lambda name: name)

records = view_expenses()
df = pd.DataFrame(records, columns=COLUMNS)
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

if page == "Dashboard":
    st.title("Your spending at a glance")
    st.caption("A clear view of your recorded expenses.")

    if df.empty:
        st.info("No expenses yet. Add your first expense to see your dashboard.")
    else:
        today = date.today()
        month_rows = df[(df["Date"].dt.year == today.year) & (df["Date"].dt.month == today.month)]
        summary = spending_summary(df)
        total = summary["total"]
        month_total = float(month_rows["Amount"].sum())
        average = summary["average"]
        with st.container(horizontal=True):
            st.metric("All-time spending", f"₹{total:,.2f}", border=True)
            st.metric("This month", f"₹{month_total:,.2f}", border=True)
            st.metric("Average transaction", f"₹{average:,.2f}", border=True)
            st.metric("Transactions", f"{summary['count']:,}", border=True)

        left, right = st.columns(2)
        with left:
            st.subheader("Spending by category")
            st.bar_chart(category_totals(df), y_label="Amount (₹)", alt="Total expense amount for each category")
        with right:
            st.subheader("Monthly spending")
            st.bar_chart(monthly_totals(df), y_label="Amount (₹)", alt="Expense totals by month")

        st.subheader("Recent transactions")
        recent = df.sort_values(["Date", "ID"], ascending=False).head(5).copy()
        recent["Date"] = recent["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(recent, hide_index=True, alt="Five most recent expenses")

elif page == "Add expense":
    st.title("Add an expense")
    st.caption("Record a purchase so you can keep track of where your money goes.")
    with st.form("expense_form", clear_on_submit=True):
        title = st.text_input("Expense title", max_chars=100, placeholder="e.g. Lunch")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
        category = st.selectbox("Category", CATEGORIES)
        expense_date = st.date_input("Date", value=date.today(), max_value=date.today())
        payment_method = st.selectbox("Payment method", PAYMENT_METHODS)
        submitted = st.form_submit_button("Save expense", type="primary")
    if submitted:
        try:
            st.success(add_new_expense(title, amount, category, expense_date.isoformat(), payment_method))
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))

else:
    st.title("Transactions")
    st.caption("Filter, export, edit, and remove your expense records.")
    if df.empty:
        st.info("No transactions recorded yet.")
    else:
        filter_col, date_col = st.columns([1, 2])
        selected_categories = filter_col.multiselect("Filter by category", CATEGORIES)
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        date_range = date_col.date_input("Date range", value=(min_date, max_date),
                                         min_value=min_date, max_value=max_date)
        filtered = df.copy()
        if selected_categories:
            filtered = filtered[filtered["Category"].isin(selected_categories)]
        if len(date_range) == 2:
            filtered = filtered[filtered["Date"].dt.date.between(date_range[0], date_range[1])]
        display = filtered.copy()
        display["Date"] = display["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(display, hide_index=True, alt="Expense transaction list")
        csv_data = display.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered transactions as CSV", csv_data,
                           file_name="smartspend_transactions.csv", mime="text/csv")

        st.subheader("Edit or delete a transaction")
        if filtered.empty:
            st.caption("No transactions match the current filters.")
        else:
            choices = filtered.sort_values("ID", ascending=False)
            selected_id = st.selectbox("Select a transaction", choices["ID"].tolist(),
                                       format_func=lambda expense_id: (
                                           f"#{expense_id} · {choices.loc[choices['ID'] == expense_id, 'Title'].iloc[0]} · "
                                           f"₹{choices.loc[choices['ID'] == expense_id, 'Amount'].iloc[0]:,.2f}"
                                       ))
            current = df.loc[df["ID"] == selected_id].iloc[0]
            with st.form("edit_expense_form"):
                new_title = st.text_input("Title", value=str(current["Title"]), max_chars=100)
                new_amount = st.number_input("Amount (₹)", min_value=0.0, value=float(current["Amount"]),
                                             step=10.0, format="%.2f")
                new_category = st.selectbox("Category", CATEGORIES,
                                            index=CATEGORIES.index(current["Category"]) if current["Category"] in CATEGORIES else 0)
                current_date = current["Date"].date()
                new_date = st.date_input("Date", value=current_date, max_value=date.today())
                new_method = st.selectbox("Payment method", PAYMENT_METHODS,
                                          index=PAYMENT_METHODS.index(current["Payment Method"])
                                          if current["Payment Method"] in PAYMENT_METHODS else 0)
                save_edit = st.form_submit_button("Save changes", type="primary")
            if save_edit:
                try:
                    st.success(edit_expense(int(selected_id), new_title, new_amount, new_category,
                                            new_date.isoformat(), new_method))
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
            if st.button("Delete selected transaction", type="secondary"):
                try:
                    st.success(remove_expense(int(selected_id)))
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

