"""
orchestrator.py  —  parallel simulation runner + aggregation
"""

import numpy as np
from joblib import Parallel, delayed
import random


def _single_worker(params, worker_seed):
    from simulation_core import simulate_one
    np.random.seed(worker_seed)
    random.seed(worker_seed)

    p        = params
    risk_np  = np.array(p['risk_levels'], dtype=np.float64)
    n_months = int(p.get('n_months', 12))
    tpm      = int(p.get('trades_per_month', max(1, int(p['num_trades']) // max(1, n_months))))

    base_wr   = p['min_win_rate']
    wrc       = p.get('win_rate_change', 0.0)
    month_mod = np.random.randint(1, 4)
    if month_mod == 1:
        base_wr -= wrc
    elif month_mod == 2:
        base_wr += wrc
    if np.random.random() < 0.10:
        base_wr -= wrc
    base_wr = min(max(base_wr, 1.0), 99.0)

    is_prop      = 1 if p['account_type'] == 2 else 0
    dd_threshold = float(p.get('max_dd_threshold', 0.0) or 0.0)

    return simulate_one(
        n_trades          = int(p['num_trades']),
        account_size      = float(p['account_size']),
        risk_levels       = risk_np,
        win_rate_base     = float(base_wr),
        lower_rr          = float(p['min_rr']),
        upper_rr          = float(p['max_rr']),
        commission        = float(p['commission']),
        be_percent        = float(p.get('break_even_pct', 0.0)),
        max_dd_threshold  = dd_threshold,
        is_prop           = int(is_prop),
        missed_trade_pct  = float(p.get('missed_trade_pct', 7.5)),
        use_kelly         = int(p.get('use_kelly', 0)),
        kelly_fraction    = float(p.get('kelly_fraction', 0.25)),
        ar1_rho           = float(p.get('ar1_rho', 0.0)),
        psych_dd_threshold= float(p.get('psych_dd_threshold', 0.0)),
        psych_reduction   = float(p.get('psych_reduction', 1.0)),
        partial_at_rr     = float(p.get('partial_at_rr', 0.0)),
        partial_fraction  = float(p.get('partial_fraction', 0.5)),
        trades_per_month  = tpm,
        n_months          = n_months,
        edge_decay_on     = int(p.get('edge_decay_on', 1)),
        decay_start       = int(p.get('decay_start', 150)),
        decay_every       = int(p.get('decay_every', 175)),
    )


def run_parallel(params: dict, n_jobs: int = -1, verbose: int = 0):
    total       = int(params['runs']) * int(params['n_people'])
    master_seed = int(params['seed'])
    seeds       = [(master_seed + i * 7919) % (2**31 - 1) for i in range(total)]
    return Parallel(n_jobs=n_jobs, verbose=verbose, prefer="processes")(
        delayed(_single_worker)(params, s) for s in seeds
    )


def aggregate_results(all_results, params):
    equity_curves    = []
    monthly_curves   = []
    final_balances   = []
    win_streaks      = []
    loss_streaks     = []
    be_streaks       = []
    all_rr           = []
    total_wins = total_losses = total_be = total_missed = total_blown = 0
    total_profit = total_loss_amt = 0.0
    exit_causes  = {0: 0, 1: 0, 2: 0}

    for res in all_results:
        if len(res) != 14:
            continue
        (equity, wins, losses, be, ws, ls, bs,
         blown, profit, loss_amt, rr_arr, missed, exit_cause,
         monthly_bal) = res

        equity_curves.append(equity)
        monthly_curves.append(monthly_bal)
        final_balances.append(float(equity[-1]))
        win_streaks.append(int(ws))
        loss_streaks.append(int(ls))
        be_streaks.append(int(bs))
        all_rr.extend(rr_arr.tolist())
        total_wins     += int(wins)
        total_losses   += int(losses)
        total_be       += int(be)
        total_missed   += int(missed)
        total_profit   += float(profit)
        total_loss_amt += float(loss_amt)
        if blown:
            total_blown += 1
        exit_causes[exit_cause] = exit_causes.get(exit_cause, 0) + 1

    max_curve_len = max(len(c) for c in equity_curves)

    return {
        "equity_curves":   equity_curves,
        "monthly_curves":  monthly_curves,
        "final_balances":  final_balances,
        "win_streaks":     win_streaks,
        "loss_streaks":    loss_streaks,
        "be_streaks":      be_streaks,
        "all_rr":          np.array(all_rr, dtype=np.float32),
        "total_wins":      total_wins,
        "total_losses":    total_losses,
        "total_be":        total_be,
        "total_missed":    total_missed,
        "total_profit":    total_profit,
        "total_loss":      total_loss_amt,
        "total_blown":     total_blown,
        "exit_causes":     exit_causes,
        "max_curve_len":   max_curve_len,
        "n_sims":          len(equity_curves),
    }
