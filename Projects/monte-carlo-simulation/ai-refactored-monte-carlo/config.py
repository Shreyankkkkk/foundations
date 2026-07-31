"""
config.py  —  user input, validation, parameter bundling
"""

import sys
import random

L_GREEN = '\033[92m'
GREEN   = '\033[32m'
RED     = '\033[91m'
YELLOW  = '\033[93m'
PURPLE  = '\033[95m'
CYAN    = '\033[96m'
ENDC    = '\033[0m'


class InputValidationError(Exception):
    pass


def _prompt_int(prompt, lo=None, hi=None, default=None):
    while True:
        try:
            raw = input(prompt).strip()
            if not raw and default is not None:
                return default
            v = int(raw)
            if lo is not None and v < lo:
                print(f"{RED}Must be >= {lo}{ENDC}")
                continue
            if hi is not None and v > hi:
                print(f"{RED}Must be <= {hi}{ENDC}")
                continue
            return v
        except ValueError:
            print(f"{RED}Please enter a whole number.{ENDC}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Cancelled.{ENDC}")
            sys.exit(0)


def _prompt_float(prompt, lo=None, hi=None, default=None):
    while True:
        try:
            raw = input(prompt).strip()
            if not raw and default is not None:
                return default
            v = float(raw)
            if lo is not None and v < lo:
                print(f"{RED}Must be >= {lo}{ENDC}")
                continue
            if hi is not None and v > hi:
                print(f"{RED}Must be <= {hi}{ENDC}")
                continue
            return v
        except ValueError:
            print(f"{RED}Please enter a number.{ENDC}")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Cancelled.{ENDC}")
            sys.exit(0)


def _prompt_yn(prompt, default='n'):
    raw = input(prompt).strip().lower()
    if not raw:
        raw = default
    return raw in ('y', 'yes', '1')


def _realism_settings(p):
    print(f"\n{PURPLE}--- Optional: Realism Settings (press Enter to keep defaults) ---{ENDC}")

    print(f"{YELLOW}  Session correlation: how much a win/loss affects the next trade's probability.")
    print(f"  0 = fully independent.  0.15 = mild intraday correlation (recommended).{ENDC}")
    p['ar1_rho'] = _prompt_float(
        f"{CYAN}  Session correlation (default 0.15): {ENDC}",
        lo=0.0, hi=0.95, default=0.15)

    use_kelly = _prompt_yn(
        f"{CYAN}  Kelly position sizing? Adjusts size based on your edge (default n): {ENDC}",
        default='n')
    p['use_kelly'] = 1 if use_kelly else 0
    p['kelly_fraction'] = _prompt_float(
        f"{CYAN}    Fraction of full Kelly, e.g. 0.25 = quarter-Kelly (default 0.25): {ENDC}",
        lo=0.05, hi=1.0, default=0.25) if use_kelly else 0.25

    print(f"{YELLOW}  Psych reduction: automatically cut size after hitting a drawdown threshold.")
    print(f"  Models the real tendency to trade smaller after losses.{ENDC}")
    use_psych = _prompt_yn(
        f"{CYAN}  Enable psychological size reduction? (default n): {ENDC}", default='n')
    if use_psych:
        p['psych_dd_threshold'] = _prompt_float(
            f"{CYAN}    Drawdown % that triggers reduction (e.g. 5): {ENDC}",
            lo=1, hi=50) / 100.0
        p['psych_reduction'] = _prompt_float(
            f"{CYAN}    Size multiplier after trigger, e.g. 0.5 = half size: {ENDC}",
            lo=0.1, hi=1.0)
    else:
        p['psych_dd_threshold'] = 0.0
        p['psych_reduction']    = 1.0

    print(f"{YELLOW}  Partial exits: close part of the position at a set RR, let the rest run.{ENDC}")
    use_partial = _prompt_yn(
        f"{CYAN}  Enable partial profit-taking? (default n): {ENDC}", default='n')
    if use_partial:
        p['partial_at_rr']    = _prompt_float(
            f"{CYAN}    Take partial at RR (e.g. 1.5): {ENDC}", lo=0.5)
        p['partial_fraction'] = _prompt_float(
            f"{CYAN}    Fraction to close at that level, e.g. 0.5 = half: {ENDC}",
            lo=0.1, hi=0.9)
    else:
        p['partial_at_rr']    = 0.0
        p['partial_fraction'] = 0.5

    # ── Edge decay ──────────────────────────────────────────────
    print(f"{YELLOW}  Edge decay: gradually erodes win rate and RR as your edge gets")
    print(f"  discovered/copied by the market. Most realistic for live trading.{ENDC}")
    use_decay = _prompt_yn(
        f"{CYAN}  Enable edge decay? (default y): {ENDC}", default='y')
    if use_decay:
        p['edge_decay_on'] = 1
        p['decay_start']   = _prompt_int(
            f"{CYAN}    Trades before decay begins (default 150): {ENDC}",
            lo=50, hi=500, default=150)
        p['decay_every']   = _prompt_int(
            f"{CYAN}    Trades between each decay event (default 175): {ENDC}",
            lo=50, hi=500, default=175)
    else:
        p['edge_decay_on'] = 0
        p['decay_start']   = 150
        p['decay_every']   = 175

    return p


def collect_params(mode='new', prev_params=None) -> dict:
    p = {}

    if mode == 'new':
        p['seed'] = random.randint(1, 1_000_000)
        print(f"{YELLOW}Seed: {p['seed']}{ENDC}")

        # ── Trade period: per month × months ──────────────────────────────
        p['trades_per_month'] = _prompt_int(
            f"{CYAN}Trades per month: {ENDC}", lo=1)
        p['n_months'] = _prompt_int(
            f"{CYAN}Number of months: {ENDC}", lo=1)
        p['num_trades'] = p['trades_per_month'] * p['n_months']
        print(f"{YELLOW}  Total trades: {p['num_trades']:,}  "
              f"({p['trades_per_month']} x {p['n_months']} months){ENDC}")

        p['runs']         = _prompt_int(f"{CYAN}Number of runs: {ENDC}", lo=1)
        p['n_people']     = _prompt_int(f"{CYAN}Number of people: {ENDC}", lo=1)
        p['account_size'] = _prompt_float(f"{CYAN}Account size ($): {ENDC}", lo=1)
        p['min_win_rate'] = _prompt_float(f"{CYAN}Minimum win rate (%): {ENDC}", lo=0, hi=100)
        p['min_rr']       = _prompt_float(f"{CYAN}Minimum RR: {ENDC}", lo=0)
        p['max_rr']       = _prompt_float(f"{CYAN}Maximum RR: {ENDC}", lo=p['min_rr'])
        p['commission']   = _prompt_float(f"{CYAN}Commission per trade ($): {ENDC}", lo=0)
        p['break_even_pct'] = _prompt_float(
            f"{CYAN}Break-even % of trades: {ENDC}", lo=0, hi=100)
        p['missed_trade_pct'] = _prompt_float(
            f"{CYAN}Missed trades % (default 7.5): {ENDC}", lo=0, hi=50, default=7.5)

        wr_var_max = 100.0 - p['min_win_rate']
        print(f"{YELLOW}  (max variance is {wr_var_max:.0f} — prevents win rate exceeding 100%){ENDC}")
        p['win_rate_change'] = _prompt_float(
            f"{CYAN}Monthly win-rate variance (0-{wr_var_max:.0f}): {ENDC}",
            lo=0, hi=wr_var_max)

        n_risk = _prompt_int(f"{CYAN}Number of risk tiers: {ENDC}", lo=1)
        risk_levels = []
        for i in range(n_risk):
            r = _prompt_float(f"{CYAN}  Risk level {i+1} (%): {ENDC}", lo=0, hi=100)
            risk_levels.append(r / 100.0)
        p['risk_levels'] = risk_levels

        p = _realism_settings(p)

    else:  # reproduce
        p = dict(prev_params)
        p['risk_levels'] = [float(r) for r in p['risk_levels_str'].split(',') if r.strip()]
        # Recalculate num_trades from monthly params if present
        if 'trades_per_month' in p and 'n_months' in p:
            p['num_trades'] = int(p['trades_per_month']) * int(p['n_months'])
        p['break_even_pct'] = _prompt_float(
            f"{CYAN}Break-even % of trades (saved: {p.get('break_even_pct', 0)}): {ENDC}",
            lo=0, hi=100, default=float(p.get('break_even_pct', 0.0)))
        p['missed_trade_pct'] = _prompt_float(
            f"{CYAN}Missed trades % (saved: {p.get('missed_trade_pct', 7.5)}): {ENDC}",
            lo=0, hi=50, default=float(p.get('missed_trade_pct', 7.5)))
        p = _realism_settings(p)

    print()
    acct = _prompt_int(f"{CYAN}Account type: (1) Live  (2) Prop firm: {ENDC}", 1, 2)
    p['account_type'] = acct
    if acct == 1:
        p['target_goal']      = _prompt_float(
            f"{CYAN}Target goal ($): {ENDC}", lo=p['account_size'])
        p['max_dd_threshold'] = 0.0
    else:
        p['max_dd_threshold'] = _prompt_float(
            f"{CYAN}Max allowed drawdown (%): {ENDC}", lo=0, hi=100) / 100.0
        p['target_goal']      = None

    return p


def params_to_db_dict(p: dict) -> dict:
    d = dict(p)
    d['risk_levels'] = ','.join(str(r) for r in p['risk_levels'])
    return d
