-- Wealth Management Demo Database Schema
-- Mock Oracle DB structure for Indian clients

CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    occupation TEXT,
    annual_income_lakhs REAL,
    tax_regime TEXT, -- 'old' or 'new'
    risk_profile TEXT, -- 'conservative', 'moderate', 'aggressive'
    pan_number TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS portfolios (
    portfolio_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    asset_type TEXT, -- 'equity', 'debt', 'gold', 'real_estate', 'cash', 'fd', 'ppf', 'epf', 'nps', 'elss'
    asset_name TEXT,
    current_value REAL,
    allocation_percent REAL,
    purchase_value REAL,
    unrealized_gains REAL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    portfolio_id INTEGER,
    transaction_type TEXT, -- 'buy', 'sell', 'dividend', 'interest'
    amount REAL,
    transaction_date DATE,
    description TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id)
);

CREATE TABLE IF NOT EXISTS tax_sections (
    section_id INTEGER PRIMARY KEY,
    section_code TEXT, -- '80C', '80D', '80CCD', etc.
    description TEXT,
    max_deduction REAL,
    applicable_regime TEXT -- 'old', 'new', 'both'
);

-- Insert tax sections for FY 2025-26
INSERT OR IGNORE INTO tax_sections (section_code, description, max_deduction, applicable_regime) VALUES
('80C', 'Investments in PPF, ELSS, LIC, NSC, etc.', 150000, 'old'),
('80CCC', 'Pension plan contributions', 150000, 'old'),
('80CCD(1)', 'NPS employee contribution (within 80C limit)', 150000, 'both'),
('80CCD(1B)', 'Additional NPS contribution', 50000, 'both'),
('80CCD(2)', 'Employer NPS contribution', 0.1, 'both'), -- 10% of salary
('80D', 'Health insurance premium', 75000, 'old'),
('80E', 'Education loan interest', 999999999, 'old'),
('80G', 'Donations to charitable institutions', 999999999, 'old'),
('80EEA', 'Home loan interest (affordable housing)', 150000, 'old'),
('80TTA', 'Savings account interest', 10000, 'old'),
('24(b)', 'Home loan interest', 200000, 'old'),
('LTCG_Equity', 'Long-term capital gains exemption on equity', 125000, 'both'),
('STCG_Equity', 'Short-term capital gains tax rate', 0.20, 'both');
