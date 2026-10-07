# Monte Carlo Simulation — Pro Edition

A professional-grade trading simulation engine built on Numba JIT + joblib parallelism.

## What changed from v1

### Critical fixes
| # | Issue | Fix |
|---|-------|-----|
| C1 | **O(n²) drawdown** — prop-firm check rescanned full equity history every trade | Rolling `peak` variable → O(1) per trade |
| C2 | **No parallelism** — all runs were sequential, one core | `joblib.Parallel(n_jobs=-1)` uses every CPU core |
| C3 | **Numba cache** — JIT recompiled on every run | `@njit(cache=True)` persists compiled code to disk |

### High priority improvements
| # | Feature | Where |
|---|---------|--------|
| H1 | Kelly Criterion / fractional-Kelly position sizing | `simulation_core._kelly_fraction` |
| H2 | AR(1) win-probability correlation between trades | `simulate_one` — `ar1_noise` term |
| H3 | GARCH(1,1) intra-regime volatility clustering | `simulation_core._garch_vol_path` |
| H4 | Psychological risk-aversion drift after drawdowns | `simulate_one` — `psych_mult` |
| H5 | Module split (was one 700-line god-file) | 6 focused files |
| H6 | Unit tests with pytest | `tests/test_metrics.py` |

### Enhancements
| # | Feature | Where |
|---|---------|--------|
| E1 | Time-of-day session effects (London/NY/Overlap) | `simulation_core._session_modifier` |
| E2 | Partial profit-taking at configurable RR milestones | `simulate_one` — `partial_at_rr` |
| E3 | AR(1) trade correlation | same as H2 |
| E4 | GARCH vol clustering | same as H3 |
| E5 | Kelly sizing | same as H1 |
| E6 | Psychological degradation | same as H4 |
| E7 | Calmar ratio added | `simulation_core.calmar_ratio` |
| E8 | Professional dark-theme 6-panel dashboard | `plotting.py` |

## File structure

```
monte_carlo_pro/
├── main.py              # Entry point
├── simulation_core.py   # Numba JIT engine (single run)
├── orchestrator.py      # joblib parallel runner + aggregation
├── metrics.py           # Analytics (percentiles, VaR, etc.)
├── plotting.py          # Dark-theme matplotlib charts
├── config.py            # User input + validation
├── database.py          # MySQL layer (optional)
├── schema.sql           # DB setup script
└── tests/
    └── test_metrics.py  # pytest unit tests
```

## Installation

```bash
pip install numba numpy scipy matplotlib seaborn pandas joblib
pip install mysql-connector-python   # optional, for DB features
pip install pytest                   # optional, for tests
```

## Run

```bash
cd monte_carlo_pro
python main.py
```

## Run tests

```bash
python -m pytest tests/ -v
# or without pytest:
python tests/test_metrics.py
```

## Speed comparison

| Version | 100M trades | Mechanism |
|---------|-------------|-----------|
| v1      | ~13 min     | Single core, O(n²) DD |
| v2      | ~90 sec†    | All cores, O(1) DD, cached JIT |

† Estimated on 8-core machine. Actual speedup = number of cores × O(n²) fix factor.

## Database setup (optional)

```bash
mysql -u root -p < schema.sql
```

Then answer `y` when asked to save run on startup.

## Key design decisions

**GARCH parameters** `ω=0.00001, α=0.09, β=0.90` are tuned for intraday returns where
volatility clusters strongly but mean-reverts within sessions. Adjust in `simulation_core._garch_vol_path`.

**Quarter-Kelly default** (25% of full Kelly) follows standard quant practice. Full Kelly is
theoretically optimal but requires perfectly known edge — real-world uncertainty warrants
the fractional version. See Thorp (2006), *The Kelly Criterion in Blackjack, Sports Betting and the Stock Market*.

**AR(1) rho=0.0 default** — set this to 0.10–0.20 for realistic intraday session correlation,
or 0.0 for independent trades.
