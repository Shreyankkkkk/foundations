"""
database.py
===========
All MySQL interaction, isolated and testable.
Uses context managers so connections are always closed.
"""

from contextlib import contextmanager
import sys

try:
    import mysql.connector as sql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False


class DatabaseError(Exception):
    pass


@contextmanager
def _connect(host, user, passwd, database, timeout=10):
    if not MYSQL_AVAILABLE:
        raise DatabaseError("mysql-connector-python not installed")
    conn = cursor = None
    try:
        conn = sql.connect(
            host=host, user=user, passwd=passwd,
            database=database, connect_timeout=timeout,
        )
        cursor = conn.cursor()
        if not conn.is_connected():
            raise DatabaseError("Connection failed immediately")
        yield conn, cursor
    except sql.Error as e:
        raise DatabaseError(f"MySQL error: {e}") from e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def save_run(host, user, passwd, database, params: dict) -> int:
    """
    Insert a new run into monte_carlo_runs.
    Returns the auto-increment run_id.
    Schema must already exist — see schema.sql.
    """
    cols = [
        "seed", "num_trades", "account_size", "min_win_rate",
        "min_rr", "max_rr", "commission", "win_rate_change",
        "risk_levels", "runs", "n_people",
        "use_kelly", "kelly_fraction",
        "ar1_rho", "psych_dd_threshold", "psych_reduction",
        "partial_at_rr", "partial_fraction",
        "missed_trade_pct", "break_even_pct",
    ]
    placeholders = ", ".join(["%s"] * len(cols))
    col_str      = ", ".join(cols)
    sql_str      = f"INSERT INTO monte_carlo_runs ({col_str}) VALUES ({placeholders})"
    values = tuple(params.get(c) for c in cols)

    with _connect(host, user, passwd, database) as (conn, cur):
        cur.execute(sql_str, values)
        conn.commit()
        return cur.lastrowid


def load_run(host, user, passwd, database, run_id: int) -> dict:
    """Fetch a previous run by ID."""
    with _connect(host, user, passwd, database) as (conn, cur):
        cur.execute("SELECT * FROM monte_carlo_runs WHERE run_id = %s", (run_id,))
        row = cur.fetchone()
        if row is None:
            raise DatabaseError(f"Run ID {run_id} not found")
        desc = [d[0] for d in cur.description]
        return dict(zip(desc, row))


SCHEMA_SQL = """
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
"""
