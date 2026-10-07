# Monte Carlo Simulation STATE

Status: active. Python trading simulation. Goal: realistic prop-firm / trading-account outcome simulation; plan to publish as a website (TODO confirm).

## Versions in repo
- `archive/`: own iterations `monte_carlo_v1.0.0.py` to `v6.0.0.py`, plus `monte_carlo_chatgpt_v6.0.0.py` and `monte_carlo_claude_v6.0.0 / v6.1.0 / v6.2.0.py` (AI-written comparison versions)
- `current/`: modular version (was `ai-refactored-monte-carlo/`). Files: `main.py` (entry), `simulation_core.py` (Numba JIT single run), `orchestrator.py` (joblib parallel + aggregation), `metrics.py`, `plotting.py`, `config.py`, `database.py` + `schema.sql` (optional MySQL), `test_metrics.py`. Its `README.md` lists what changed from v1.

## Features (from the refactor README)
O(1) rolling-peak drawdown, all-core parallelism, cached JIT, fractional Kelly sizing, AR(1) trade correlation, GARCH(1,1) volatility clustering, psychological drawdown drift, session effects (London/NY/Overlap), partial profit-taking, Calmar ratio, 6-panel dark dashboard, pytest unit tests.

## Model parameters (value | justification | status)
| Parameter | Value | Justification given | Status |
|---|---|---|---|
| GARCH omega, alpha, beta | 0.00001, 0.09, 0.90 | "tuned for intraday returns" (README), no derivation shown | TODO: derive or fit from real data |
| Kelly fraction default | 0.25 | standard quant practice, Thorp (2006) | convention, not calibrated |
| AR(1) rho default | 0.0 (suggested 0.10-0.20) | README note | ASSUMED |

## Known issues / TODO
- Shorten the repo layout mismatch: README says `monte_carlo_pro/` and `tests/` but files sit flat in `current/`
- `__pycache__` was committed in `current/` (now gitignored); if it is still tracked, run `git rm -r --cached projects/monte-carlo-simulation/current/__pycache__`
- Calibrate parameters against real trade data from the trading journal
- Publish as a website (plan)
