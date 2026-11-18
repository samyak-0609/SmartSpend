# SmartSpend — personal expense tracker

SmartSpend is a small Python and Streamlit utility for recording everyday expenses. It saves transactions in a local SQLite database, summarizes spending, and lets you filter, export, edit, and delete records.

## Features

- Add expenses with a title, amount, category, date, and payment method.
- Review all transactions and filter them by category and date range.
- Edit or delete a selected transaction.
- View all-time and current-month totals, average transaction size, and transaction count.
- See spending charts by category and month.
- Export the currently filtered transaction list to CSV.
- Store data locally in SQLite; no account or API key is required.

## Run locally

Use Python 3.10 or newer. From this project folder, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux, activate with `source .venv/bin/activate`. The app opens at `http://localhost:8501`.

SmartSpend creates `expenses.db` beside `database.py` the first time it runs. Keep a backup of this file if you need to preserve local records. It is excluded from Git because it may contain personal spending data.

## Run checks

Install development dependencies and run the automated tests:

```powershell
python -m pip install -r dev-requirements.txt
python -m pytest
```

## Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit user interface |
| `analytics.py` | Reusable spending summaries |
| `expense.py` | Expense validation and business rules |
| `database.py` | SQLite schema and data operations |
| `test_db.py`, `test_expense.py` | Automated tests using a temporary database |

## GitHub and deployment

The public source repository is [github.com/samyak-0609/SmartSpend](https://github.com/samyak-0609/SmartSpend).

To publish the app, sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub, choose **Create app**, select the `samyak-0609/SmartSpend` repository and `main` branch, and enter `app.py` as the app file. Choose an available app URL and deploy.

Community Cloud installs the packages listed in `requirements.txt`. The app's SQLite file is local to its runtime; treat the hosted app as a demo and do not rely on that file as durable cloud storage. For long-term shared storage, connect a hosted database before using it with important records.

## Notes

- Amounts are displayed in Indian rupees (₹); the app does not perform currency conversion.
- This is a single-user utility. It has no login or multi-user access controls.
- Do not commit a real `expenses.db` file or secrets to a public repository.

