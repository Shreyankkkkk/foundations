"""
tests/test_metrics.py
=====================
[HIGH-6]  Unit tests for simulation_core metrics and orchestrator aggregation.
Run with:
    cd monte_carlo_pro
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pytest

# ── simulation_core metric tests ─────────────────────────────────────────────

def test_max_drawdown_flat():
    from simulation_core import max_drawdown
    curve = np.array([1000.0, 1000.0, 1000.0], dtype=np.float64)
    assert max_drawdown(curve) == 0.0


def test_max_drawdown_50pct():
    from simulation_core import max_drawdown
    curve = np.array([1000.0, 500.0], dtype=np.float64)
    assert abs(max_drawdown(curve) - 0.5) < 1e-9


def test_max_drawdown_recovery():
    """Peak was 1000, dropped to 800, recovered to 1200 — max DD is 20%."""
    from simulation_core import max_drawdown
    curve = np.array([1000.0, 800.0, 1200.0], dtype=np.float64)
    assert abs(max_drawdown(curve) - 0.20) < 1e-9


def test_max_drawdown_monotone_rise():
    from simulation_core import max_drawdown
    curve = np.array([100.0, 200.0, 300.0, 400.0], dtype=np.float64)
    assert max_drawdown(curve) == 0.0


def test_time_under_water_zero():
    from simulation_core import time_under_water
    curve = np.array([100.0, 200.0, 300.0], dtype=np.float64)
    assert time_under_water(curve) == 0


def test_time_under_water_basic():
    from simulation_core import time_under_water
    # Peak at index 0 (100), then 3 trades below, then recovery
    curve = np.array([100.0, 80.0, 70.0, 60.0, 110.0], dtype=np.float64)
    assert time_under_water(curve) == 3


def test_sharpe_zero_std():
    from simulation_core import sharpe_ratio
    curve = np.array([1000.0, 1000.0, 1000.0], dtype=np.float64)
    assert sharpe_ratio(curve) == 0.0


def test_sharpe_positive():
    from simulation_core import sharpe_ratio
    rng   = np.random.default_rng(42)
    curve = np.cumsum(rng.uniform(0.5, 1.5, 200)) + 1000.0
    sr    = sharpe_ratio(curve)
    assert sr > 0.0


def test_sortino_no_downside():
    from simulation_core import sortino_ratio
    curve = np.array([100.0, 110.0, 120.0, 130.0], dtype=np.float64)
    assert sortino_ratio(curve) == 0.0


def test_calmar_zero_drawdown():
    from simulation_core import calmar_ratio
    curve = np.array([100.0, 110.0, 120.0], dtype=np.float64)
    # No drawdown → calmar is 0 (guard clause)
    assert calmar_ratio(curve) == 0.0


# ── Kelly fraction tests ──────────────────────────────────────────────────────

def test_kelly_positive_edge():
    from simulation_core import _kelly_fraction
    # 55% win rate, 2.0 RR → positive Kelly
    k = _kelly_fraction(55.0, 2.0, 0.25)
    assert 0.1 <= k <= 2.0


def test_kelly_negative_edge():
    from simulation_core import _kelly_fraction
    # 30% win rate, 1.0 RR → negative Kelly → f clamped to 0.05 → mult = 0.2
    k = _kelly_fraction(30.0, 1.0, 0.25)
    assert k == pytest.approx(0.2)   # 0.05 / 0.25 = 0.2, above 0.1 floor


def test_kelly_caps_at_2():
    from simulation_core import _kelly_fraction
    # 95% win rate, 10 RR → very high Kelly → capped at 2.0
    k = _kelly_fraction(95.0, 10.0, 1.0)
    assert k <= 2.0


# ── metrics.py tests ─────────────────────────────────────────────────────────

def test_portfolio_metrics_basic():
    import metrics as M
    balances    = [1200.0, 800.0, 1000.0, 1500.0, 950.0]
    account     = 1000.0
    result      = M.portfolio_metrics(balances, account)
    assert 0.0 <= result['prob_ruin'] <= 100.0
    assert 0.0 <= result['prob_profit'] <= 100.0
    assert result['max_final'] == 1500.0
    assert result['min_final'] == 800.0


def test_rr_stats_empty():
    import metrics as M
    result = M.rr_stats(np.array([]))
    assert result == {}


def test_rr_stats_values():
    import metrics as M
    rr = [1.5, 2.0, 2.5, 1.5, 1.5]
    result = M.rr_stats(rr)
    assert result['mean'] == pytest.approx(np.mean(rr), rel=1e-3)
    assert result['most_common'] == 1.5


def test_drawdown_stats():
    import metrics as M
    mdds = [0.05, 0.10, 0.15, 0.20]
    tuws = [10, 20, 30, 40]
    result = M.drawdown_stats(mdds, tuws)
    assert result['avg_mdd_pct'] == pytest.approx(12.5, rel=1e-3)
    assert result['worst_tuw']   == 40


def test_streak_stats():
    import metrics as M
    result = M.streak_stats([3, 5, 7], [2, 4, 6], [1, 2, 3])
    assert result['avg_win_streak']  == pytest.approx(5.0, rel=1e-3)
    assert result['max_loss_streak'] == 6


# ── Full simulation smoke test ────────────────────────────────────────────────

def test_simulate_one_runs():
    """Basic smoke test: simulate_one should return 13-element tuple."""
    from simulation_core import simulate_one
    risk = np.array([0.01, 0.005])
    result = simulate_one(
        n_trades=50, account_size=10000.0, risk_levels=risk,
        win_rate_base=55.0, lower_rr=1.0, upper_rr=3.0,
        commission=2.0, be_percent=5.0, max_dd_threshold=0.0,
        is_prop=0, missed_trade_pct=7.5,
        use_kelly=0, kelly_fraction=0.25,
        ar1_rho=0.0, psych_dd_threshold=0.0, psych_reduction=1.0,
        partial_at_rr=0.0, partial_fraction=0.5,
    )
    assert len(result) == 13
    equity = result[0]
    assert equity[0] == 10000.0
    assert len(equity) >= 1


def test_simulate_one_prop_firm():
    """Prop firm mode should blow up on extreme DD."""
    from simulation_core import simulate_one
    risk   = np.array([0.50])   # 50% risk — will blow up quickly
    result = simulate_one(
        n_trades=200, account_size=10000.0, risk_levels=risk,
        win_rate_base=30.0, lower_rr=0.5, upper_rr=1.0,
        commission=0.0, be_percent=0.0, max_dd_threshold=0.05,
        is_prop=1, missed_trade_pct=0.0,
        use_kelly=0, kelly_fraction=0.25,
        ar1_rho=0.0, psych_dd_threshold=0.0, psych_reduction=1.0,
        partial_at_rr=0.0, partial_fraction=0.5,
    )
    blown = result[7]
    assert blown == 1, "Should have failed prop firm with 50% risk at 30% win rate"


def test_simulate_one_kelly():
    """Kelly mode should not crash and should produce valid equity."""
    from simulation_core import simulate_one
    risk = np.array([0.01])
    result = simulate_one(
        n_trades=100, account_size=10000.0, risk_levels=risk,
        win_rate_base=55.0, lower_rr=1.5, upper_rr=3.0,
        commission=1.0, be_percent=5.0, max_dd_threshold=0.0,
        is_prop=0, missed_trade_pct=5.0,
        use_kelly=1, kelly_fraction=0.25,
        ar1_rho=0.15, psych_dd_threshold=0.05, psych_reduction=0.5,
        partial_at_rr=1.5, partial_fraction=0.5,
    )
    assert len(result) == 13
    equity = result[0]
    assert not np.any(np.isnan(equity))
    assert not np.any(np.isinf(equity))


if __name__ == "__main__":
    # Run tests without pytest for quick verification
    import traceback
    funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for f in funcs:
        try:
            f()
            print(f"  \033[92mPASS\033[0m  {f.__name__}")
            passed += 1
        except Exception:
            print(f"  \033[91mFAIL\033[0m  {f.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
