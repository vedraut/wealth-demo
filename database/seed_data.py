"""
Seed data module for the Wealth Management & Tax Advisory Demo.

Creates a SQLite database with 3 realistic Indian client profiles including:
- Personal details
- Multi-asset portfolios (equity, debt, gold, FD, PPF, EPF, NPS, ELSS, real estate)
- Realistic unrealized gains/losses for tax analysis
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "wealth_demo.db")


def get_connection() -> sqlite3.Connection:
    """Return a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Initialize database schema."""
    cursor = conn.cursor()

    # Clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            occupation TEXT NOT NULL,
            annual_income_lakhs REAL NOT NULL,
            tax_regime TEXT NOT NULL,  -- old or new
            pan TEXT UNIQUE,
            city TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Holdings table - individual securities/instruments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            holding_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            asset_type TEXT NOT NULL,  -- equity, debt, gold, fd, ppf, epf, nps, elss, real_estate
            instrument_name TEXT NOT NULL,
            units REAL NOT NULL,
            avg_buy_price REAL NOT NULL,
            current_price REAL NOT NULL,
            invested_amount REAL NOT NULL,
            current_value REAL NOT NULL,
            unrealized_pnl REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            is_tax_saver INTEGER DEFAULT 0,  -- 1 for 80C eligible
            lock_in_years INTEGER DEFAULT 0,
            FOREIGN KEY (client_id) REFERENCES clients(client_id)
        )
    """)

    # Tax deductions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tax_deductions (
            deduction_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            section TEXT NOT NULL,  -- 80C, 80D, 80G, etc.
            description TEXT,
            amount REAL NOT NULL,
            financial_year TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(client_id)
        )
    """)

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            txn_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            holding_id INTEGER,
            txn_type TEXT NOT NULL,  -- buy, sell, dividend, interest
            amount REAL NOT NULL,
            txn_date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (holding_id) REFERENCES holdings(holding_id)
        )
    """)

    conn.commit()


def seed_clients(conn: sqlite3.Connection) -> list[int]:
    """Insert 3 Indian client profiles and return their IDs."""
    cursor = conn.cursor()
    clients = [
        {
            "name": "Rajesh Mehta",
            "age": 52,
            "occupation": "Business Owner",
            "annual_income_lakhs": 120.0,
            "tax_regime": "old",
            "pan": "ABCDE1234F",
            "city": "Mumbai",
        },
        {
            "name": "Priya Sharma",
            "age": 35,
            "occupation": "IT Professional",
            "annual_income_lakhs": 50.0,
            "tax_regime": "new",
            "pan": "FGHIJ5678K",
            "city": "Bangalore",
        },
        {
            "name": "Amitabh Khanna",
            "age": 45,
            "occupation": "CXO - MNC",
            "annual_income_lakhs": 220.0,
            "tax_regime": "old",
            "pan": "KLMNO9012P",
            "city": "Delhi",
        },
    ]

    client_ids = []
    for client in clients:
        cursor.execute(
            """
            INSERT INTO clients (name, age, occupation, annual_income_lakhs, tax_regime, pan, city)
            VALUES (:name, :age, :occupation, :annual_income_lakhs, :tax_regime, :pan, :city)
            """,
            client,
        )
        client_ids.append(cursor.lastrowid)

    conn.commit()
    return client_ids


def seed_holdings(conn: sqlite3.Connection, client_ids: list[int]) -> None:
    """Seed portfolio holdings for each client."""
    cursor = conn.cursor()

    # Helper to calculate P&L
    def holding(
        client_id: int,
        asset_type: str,
        instrument: str,
        units: float,
        avg_buy: float,
        current: float,
        purchase_date: str,
        is_tax_saver: int = 0,
        lock_in: int = 0,
    ) -> dict:
        invested = units * avg_buy
        current_val = units * current
        return {
            "client_id": client_id,
            "asset_type": asset_type,
            "instrument_name": instrument,
            "units": units,
            "avg_buy_price": avg_buy,
            "current_price": current,
            "invested_amount": invested,
            "current_value": current_val,
            "unrealized_pnl": current_val - invested,
            "purchase_date": purchase_date,
            "is_tax_saver": is_tax_saver,
            "lock_in_years": lock_in,
        }

    # --- Client 1: Rajesh Mehta (Business Owner, ₹1.2Cr income) ---
    rajesh = client_ids[0]
    rajesh_holdings = [
        # Equity - diversified
        holding(rajesh, "equity", "Reliance Industries", 500, 2450.0, 2890.0, "2022-03-15"),
        holding(rajesh, "equity", "TCS Ltd", 200, 3200.0, 4150.0, "2021-08-10"),
        holding(rajesh, "equity", "HDFC Bank", 400, 1420.0, 1680.0, "2022-01-20"),
        holding(rajesh, "equity", "Infosys", 600, 1350.0, 1180.0, "2023-04-05"),  # loss
        # Debt
        holding(rajesh, "debt", "SBI Corporate Bond Fund", 2500, 12.5, 13.8, "2021-06-01"),
        holding(rajesh, "debt", "HDFC Short Term Debt", 1800, 45.2, 47.1, "2022-09-12"),
        # Gold
        holding(rajesh, "gold", "Sovereign Gold Bond 2021", 50, 4780.0, 7250.0, "2021-05-20", lock_in=8),
        holding(rajesh, "gold", "Gold ETF", 100, 5120.0, 7180.0, "2022-11-10"),
        # Fixed Deposit
        holding(rajesh, "fd", "ICICI FD 3-Year", 1, 5000000.0, 5000000.0, "2023-01-15", lock_in=3),
        # Tax savers
        holding(rajesh, "ppf", "Public Provident Fund", 1, 150000.0, 150000.0, "2020-04-01", is_tax_saver=1, lock_in=15),
        holding(rajesh, "elss", "Axis Long Term Equity", 2000, 18.5, 22.3, "2023-03-10", is_tax_saver=1, lock_in=3),
        holding(rajesh, "nps", "National Pension Scheme Tier-I", 1, 50000.0, 50000.0, "2022-04-01", is_tax_saver=1, lock_in=60),
        # Real Estate
        holding(rajesh, "real_estate", "Andheri West Apartment", 1, 8500000.0, 12500000.0, "2019-07-01"),
    ]

    # --- Client 2: Priya Sharma (Salaried IT, ₹50L income) ---
    priya = client_ids[1]
    priya_holdings = [
        # Equity
        holding(priya, "equity", "Nifty 50 ETF", 300, 195.0, 248.0, "2023-01-10"),
        holding(priya, "equity", "Tata Motors", 250, 420.0, 950.0, "2022-06-15"),
        holding(priya, "equity", "HCL Tech", 150, 1050.0, 980.0, "2023-08-20"),  # loss
        # Debt
        holding(priya, "debt", "Liquid Bees", 500, 1000.0, 1000.0, "2023-02-01"),
        # Gold
        holding(priya, "gold", "Digital Gold - Paytm", 25, 5200.0, 7180.0, "2023-10-05"),
        # FD
        holding(priya, "fd", "HDFC FD 2-Year", 1, 800000.0, 800000.0, "2024-01-01", lock_in=2),
        # Tax savers
        holding(priya, "epf", "Employee Provident Fund", 1, 420000.0, 420000.0, "2019-04-01", is_tax_saver=1, lock_in=5),
        holding(priya, "elss", "Mirae Asset Tax Saver", 1500, 28.0, 32.5, "2024-02-15", is_tax_saver=1, lock_in=3),
        holding(priya, "ppf", "Public Provident Fund", 1, 50000.0, 50000.0, "2023-04-01", is_tax_saver=1, lock_in=15),
        # NPS
        holding(priya, "nps", "NPS Tier-I (Aggressive)", 1, 25000.0, 25000.0, "2023-04-01", is_tax_saver=1, lock_in=60),
    ]

    # --- Client 3: Amitabh Khanna (CXO, ₹2.2Cr income - HNI) ---
    amitabh = client_ids[2]
    amitabh_holdings = [
        # Large equity portfolio
        holding(amitabh, "equity", "Reliance Industries", 2000, 2100.0, 2890.0, "2020-03-15"),
        holding(amitabh, "equity", "TCS Ltd", 800, 2800.0, 4150.0, "2020-06-10"),
        holding(amitabh, "equity", "HDFC Bank", 1500, 1200.0, 1680.0, "2021-01-20"),
        holding(amitabh, "equity", "Bharti Airtel", 1000, 680.0, 1120.0, "2021-09-05"),
        holding(amitabh, "equity", "Adani Enterprises", 500, 1800.0, 1200.0, "2022-11-20"),  # significant loss
        holding(amitabh, "equity", "ITC Ltd", 1200, 215.0, 420.0, "2020-02-10"),
        holding(amitabh, "equity", "Larsen & Toubro", 600, 1450.0, 3580.0, "2020-04-15"),
        # International equity
        holding(amitabh, "equity", "Motilal Oswal Nasdaq 100", 500, 95.0, 128.0, "2022-01-10"),
        # Debt
        holding(amitabh, "debt", "SBI Banking & PSU Fund", 5000, 18.5, 20.2, "2021-04-01"),
        holding(amitabh, "debt", "Corporate FD - Bajaj", 1, 3000000.0, 3000000.0, "2023-06-01", lock_in=5),
        # Gold
        holding(amitabh, "gold", "Sovereign Gold Bond 2020", 200, 4650.0, 7250.0, "2020-05-15", lock_in=8),
        holding(amitabh, "gold", "Sovereign Gold Bond 2022", 100, 5200.0, 7180.0, "2022-06-20", lock_in=8),
        # Tax savers
        holding(amitabh, "ppf", "Public Provident Fund", 1, 450000.0, 450000.0, "2018-04-01", is_tax_saver=1, lock_in=15),
        holding(amitabh, "elss", "Canara Robeco Equity Tax Saver", 3000, 22.0, 28.5, "2023-03-01", is_tax_saver=1, lock_in=3),
        holding(amitabh, "nps", "NPS Tier-I (Auto Choice)", 1, 200000.0, 200000.0, "2020-04-01", is_tax_saver=1, lock_in=60),
        # Real Estate
        holding(amitabh, "real_estate", "Gurgaon Villa", 1, 35000000.0, 52000000.0, "2018-03-01"),
        holding(amitabh, "real_estate", "Noida Commercial Plot", 1, 15000000.0, 18500000.0, "2021-08-15"),
    ]

    all_holdings = rajesh_holdings + priya_holdings + amitabh_holdings
    for h in all_holdings:
        cursor.execute(
            """
            INSERT INTO holdings (
                client_id, asset_type, instrument_name, units, avg_buy_price, current_price,
                invested_amount, current_value, unrealized_pnl, purchase_date,
                is_tax_saver, lock_in_years
            ) VALUES (
                :client_id, :asset_type, :instrument_name, :units, :avg_buy_price, :current_price,
                :invested_amount, :current_value, :unrealized_pnl, :purchase_date,
                :is_tax_saver, :lock_in_years
            )
            """,
            h,
        )

    conn.commit()


def seed_tax_deductions(conn: sqlite3.Connection, client_ids: list[int]) -> None:
    """Seed existing tax deductions for FY 2025-26."""
    cursor = conn.cursor()
    fy = "2025-26"

    deductions = [
        # Rajesh
        (client_ids[0], "80C", "ELSS + PPF + NPS", 200000),
        (client_ids[0], "80D", "Health Insurance (Family + Parents)", 50000),
        (client_ids[0], "80G", "Donation to PM CARES", 25000),
        # Priya
        (client_ids[1], "80C", "EPF + ELSS + PPF", 150000),
        (client_ids[1], "80D", "Health Insurance", 25000),
        (client_ids[1], "80CCD(1B)", "Additional NPS", 50000),
        # Amitabh
        (client_ids[2], "80C", "PPF + ELSS + NPS", 150000),
        (client_ids[2], "80D", "Health Insurance (Senior Parents)", 75000),
        (client_ids[2], "80G", "Charitable Trust", 100000),
        (client_ids[2], "80CCD(1B)", "Additional NPS", 50000),
    ]

    for client_id, section, desc, amount in deductions:
        cursor.execute(
            """
            INSERT INTO tax_deductions (client_id, section, description, amount, financial_year)
            VALUES (?, ?, ?, ?, ?)
            """,
            (client_id, section, desc, amount, fy),
        )

    conn.commit()


def seed_transactions(conn: sqlite3.Connection, client_ids: list[int]) -> None:
    """Seed recent transactions for realism."""
    cursor = conn.cursor()

    txns = [
        # Rajesh - recent dividend/interest
        (client_ids[0], None, "interest", 185000, "2025-03-31", "ICICI FD Interest Q4"),
        (client_ids[0], None, "dividend", 42000, "2025-02-15", "Reliance Dividend"),
        (client_ids[0], None, "dividend", 28000, "2025-02-20", "TCS Dividend"),
        # Priya
        (client_ids[1], None, "interest", 52000, "2025-03-31", "HDFC FD Interest"),
        (client_ids[1], None, "dividend", 15000, "2025-03-10", "Nifty ETF Dividend"),
        # Amitabh
        (client_ids[2], None, "interest", 285000, "2025-03-31", "Bajaj FD Interest"),
        (client_ids[2], None, "dividend", 185000, "2025-02-15", "Reliance Dividend"),
        (client_ids[2], None, "dividend", 125000, "2025-02-20", "TCS Dividend"),
        (client_ids[2], None, "dividend", 85000, "2025-03-05", "ITC Dividend"),
    ]

    for client_id, holding_id, txn_type, amount, txn_date, notes in txns:
        cursor.execute(
            """
            INSERT INTO transactions (client_id, holding_id, txn_type, amount, txn_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (client_id, holding_id, txn_type, amount, txn_date, notes),
        )

    conn.commit()


def create_database() -> str:
    """Create and seed the full database. Returns path to DB file."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    try:
        init_schema(conn)
        client_ids = seed_clients(conn)
        seed_holdings(conn, client_ids)
        seed_tax_deductions(conn, client_ids)
        seed_transactions(conn, client_ids)
        print(f"✅ Database created at {DB_PATH}")
        print(f"   - 3 clients seeded")
        print(f"   - {len(client_ids)} portfolios with multi-asset holdings")
        print(f"   - Tax deductions for FY 2025-26")
        return DB_PATH
    finally:
        conn.close()


def get_client_summary(conn: sqlite3.Connection, client_id: int) -> dict:
    """Get a quick summary of a client's portfolio."""
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
    client = dict(cursor.fetchone())

    cursor.execute(
        """
        SELECT asset_type, SUM(current_value) as value, SUM(unrealized_pnl) as pnl
        FROM holdings WHERE client_id = ? GROUP BY asset_type
        """,
        (client_id,),
    )
    asset_summary = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        "SELECT SUM(current_value) as total FROM holdings WHERE client_id = ?",
        (client_id,),
    )
    total_value = cursor.fetchone()["total"] or 0

    cursor.execute(
        "SELECT SUM(unrealized_pnl) as total_pnl FROM holdings WHERE client_id = ?",
        (client_id,),
    )
    total_pnl = cursor.fetchone()["total_pnl"] or 0

    return {
        "client": client,
        "total_portfolio_value": total_value,
        "total_unrealized_pnl": total_pnl,
        "asset_breakdown": asset_summary,
    }


if __name__ == "__main__":
    create_database()
