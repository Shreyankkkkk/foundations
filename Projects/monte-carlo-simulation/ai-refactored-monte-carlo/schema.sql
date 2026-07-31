-- schema.sql
-- Run once to set up the database:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS monte_carlo;
USE monte_carlo;

CREATE TABLE IF NOT EXISTS monte_carlo_runs (
    run_id              INT AUTO_INCREMENT PRIMARY KEY,
    seed                INT NOT NULL,
    num_trades          INT NOT NULL,
    account_size        DOUBLE NOT NULL,
    min_win_rate        DOUBLE NOT NULL,
    min_rr              DOUBLE NOT NULL,
    max_rr              DOUBLE NOT NULL,
    commission          DOUBLE DEFAULT 0,
    win_rate_change     DOUBLE DEFAULT 0,
    risk_levels         TEXT NOT NULL,
    runs                INT NOT NULL,
    n_people            INT NOT NULL,
    use_kelly           TINYINT DEFAULT 0,
    kelly_fraction      DOUBLE DEFAULT 0.25,
    ar1_rho             DOUBLE DEFAULT 0.0,
    psych_dd_threshold  DOUBLE DEFAULT 0.0,
    psych_reduction     DOUBLE DEFAULT 1.0,
    partial_at_rr       DOUBLE DEFAULT 0.0,
    partial_fraction    DOUBLE DEFAULT 0.5,
    missed_trade_pct    DOUBLE DEFAULT 7.5,
    break_even_pct      DOUBLE DEFAULT 0.0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
