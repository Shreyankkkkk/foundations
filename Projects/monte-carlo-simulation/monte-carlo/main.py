"""
main.py  —  entry point
"""

import sys
import traceback
import random
import numpy as np
from datetime import datetime

GREEN   = '\033[32m'
L_GREEN = '\033[92m'
RED     = '\033[91m'
L_RED   = '\033[31m'
YELLOW  = '\033[93m'
PURPLE  = '\033[95m'
CYAN    = '\033[96m'
BOLD    = '\033[1m'
DIM     = '\033[2m'
ENDC    = '\033[0m'

W = 62


def _line(char='─'):
    return f"{DIM}{char * W}{ENDC}"

def _header(title):
    pad  = (W - len(title) - 2) // 2
    side = '─' * pad
    return f"{DIM}{side}{ENDC}  {BOLD}{title}{ENDC}  {DIM}{side}{ENDC}"

def _row(label, value, value_colour=ENDC, width=38):
    dots = '.' * (width - len(label))
    return f"  {DIM}{label}{ENDC}{DIM}{dots}{ENDC}  {value_colour}{value}{ENDC}"


def _print_results(agg, params, portfolio_m, dd_m, streak_m, ratio_m, rr_m):
    p      = params
    n_sims = agg['n_sims']

    lines = ['', _line(), '']
    lines += [_header("Risk Metrics"), '']
    lines += [
        _row("5% Value at Risk",                    f"{portfolio_m['var_5']:.4f}", RED),
        _row("Expected Shortfall (CVaR)",            f"{portfolio_m['expected_shortfall']:.4f}", RED),
        _row("Probability of ruin  (<50% account)", f"{portfolio_m['prob_ruin']:.2f}%", RED),
        _row("Probability of profit",               f"{portfolio_m['prob_profit']:.2f}%", L_GREEN),
        _row("Probability of doubling account",     f"{portfolio_m['prob_double']:.2f}%", L_GREEN),
        '',
    ]
    lines += [_header("Final Balance Distribution"), '']
    lines += [
        _row("Maximum",  f"${portfolio_m['max_final']:>13,.2f}", GREEN),
        _row("Mean",     f"${portfolio_m['mean_final']:>13,.2f}", YELLOW),
        _row("Median",   f"${portfolio_m['median_final']:>13,.2f}", YELLOW),
        _row("Minimum",  f"${portfolio_m['min_final']:>13,.2f}", RED),
        '',
    ]
    lines += [_header("Drawdown"), '']
    lines += [
        _row("Average max drawdown",      f"{dd_m['avg_mdd_pct']:.2f}%", L_RED),
        _row("Worst max drawdown",        f"{dd_m['worst_mdd_pct']:.2f}%", RED),
        _row("95th percentile drawdown",  f"{dd_m['p95_mdd_pct']:.2f}%", L_RED),
        _row("Average time under water",  f"{dd_m['avg_tuw_trades']:.1f} trades", YELLOW),
        '',
    ]
    lines += [_header("Streak Analysis"), '']
    lines += [
        _row("Avg longest win streak",
             f"{streak_m['avg_win_streak']:.1f}  (worst: {streak_m['max_win_streak']})", L_GREEN),
        _row("Avg longest break-even streak",
             f"{streak_m['avg_be_streak']:.1f}  (worst: {streak_m['max_be_streak']})", YELLOW),
        _row("Avg longest loss streak",
             f"{streak_m['avg_loss_streak']:.1f}  (worst: {streak_m['max_loss_streak']})", L_RED),
        '',
    ]
    lines += [_header("Risk-Adjusted Returns"), '']
    lines += [
        _row("Average Sharpe ratio",  f"{ratio_m['avg_sharpe']:.4f}", CYAN),
        _row("Average Sortino ratio", f"{ratio_m['avg_sortino']:.4f}", CYAN),
        _row("Average Calmar ratio",  f"{ratio_m['avg_calmar']:.4f}", CYAN),
        '',
    ]

    executed  = agg['total_wins'] + agg['total_losses'] + agg['total_be']
    attempted = int(p['runs']) * int(p['n_people']) * int(p['num_trades'])
    wp  = (agg['total_wins'] / executed * 100) if executed > 0 else 0.0
    pf  = (agg['total_profit'] / agg['total_loss']) if agg['total_loss'] > 0 else float('inf')
    mp  = agg['total_missed'] / attempted * 100 if attempted > 0 else 0.0
    wr_col = L_GREEN if wp >= float(p['min_win_rate']) else RED

    lines += [_header("Trade Statistics"), '']
    lines += [
        _row("Trades attempted",              f"{attempted:,}", DIM),
        _row("Trades executed",               f"{executed:,}", ENDC),
        _row("Trades missed",                 f"{agg['total_missed']:,}  ({mp:.1f}%)", YELLOW),
        _row("Wins",                          f"{agg['total_wins']:,}", L_GREEN),
        _row("Break-evens",                   f"{agg['total_be']:,}", YELLOW),
        _row("Losses",                        f"{agg['total_losses']:,}", L_RED),
        '',
        _row("Realised win rate",             f"{wp:.2f}%", wr_col),
        _row("Global profit factor",          f"{pf:.3f}", CYAN),
        '',
    ]
    lines += [_header("Risk : Reward"), '']
    lines += [
        _row("Mean RR",                   f"{rr_m['mean']:.3f}", ENDC),
        _row("Median RR",                 f"{rr_m['median']:.3f}", ENDC),
        _row("Most common RR",            f"{rr_m['most_common']:.1f}", ENDC),
        _row("5th / 95th percentile RR",  f"{rr_m['p5']:.2f}  /  {rr_m['p95']:.2f}", DIM),
        '',
    ]

    if p.get('account_type') == 2:
        passed = n_sims - agg['total_blown']
        lines += [_header("Prop Firm Results"), '']
        lines += [
            _row(f"Failed  (>={p['max_dd_threshold']*100:.0f}% DD)",
                 f"{agg['total_blown']:,}  ({agg['total_blown']/n_sims*100:.1f}%)", RED),
            _row("Passed",
                 f"{passed:,}  ({passed/n_sims*100:.1f}%)", L_GREEN),
            '',
        ]
    elif p.get('target_goal') and p.get('target_goal') > 0:
        fb  = np.array(agg['final_balances'])
        met = int(np.sum(fb >= p['target_goal']))
        lines += [_header("Target Goal"), '']
        lines += [
            _row(f"Reached ${p['target_goal']:,.0f}",
                 f"{met:,}  ({met/n_sims*100:.1f}%)", L_GREEN),
            '',
        ]

    lines += [_line(), '']
    print('\n'.join(lines))


def main():
    start = datetime.now()
    print(f"\n{DIM}{start.strftime('%Y-%m-%d  %H:%M:%S')}{ENDC}\n")

    from config import collect_params

    mode = input(f"{CYAN}(1) New run  /  (2) Reproduce previous: {ENDC}").strip()

    params = None
    if mode == '2':
        try:
            from database import load_run
            pwd  = input(f"{PURPLE}DB password: {ENDC}")
            rid  = int(input(f"{CYAN}Run ID: {ENDC}"))
            prev = load_run('localhost', 'root', pwd, 'monte_carlo', rid)
            prev['risk_levels_str'] = prev.get('risk_levels', '0.01')
            for _k in ('account_size','min_win_rate','min_rr','max_rr','commission',
                       'win_rate_change','missed_trade_pct','break_even_pct',
                       'kelly_fraction','ar1_rho','psych_dd_threshold',
                       'psych_reduction','partial_at_rr','partial_fraction'):
                if _k in prev and prev[_k] is not None:
                    prev[_k] = float(prev[_k])
            for _k in ('num_trades','runs','n_people','use_kelly',
                       'trades_per_month','n_months'):
                if _k in prev and prev[_k] is not None:
                    prev[_k] = int(prev[_k])
            params = collect_params(mode='repro', prev_params=prev)
        except Exception as e:
            print(f"{RED}DB error: {e}  — starting fresh.{ENDC}")

    if params is None:
        params = collect_params(mode='new')

    try:
        from database import MYSQL_AVAILABLE
        if MYSQL_AVAILABLE:
            save_yn = input(f"\n{CYAN}Save to database? (y/n, default n): {ENDC}").strip().lower()
            if save_yn == 'y':
                from database import save_run
                pwd = input(f"{PURPLE}DB password: {ENDC}")
                from config import params_to_db_dict
                rid = save_run('localhost', 'root', pwd, 'monte_carlo', params_to_db_dict(params))
                print(f"{GREEN}Saved as Run ID {rid}{ENDC}")
    except Exception:
        pass

    np.random.seed(params['seed'])
    random.seed(params['seed'])

    print(f"\n{DIM}Compiling simulation kernel...{ENDC}", end='', flush=True)
    from simulation_core import simulate_one
    simulate_one(10, 1000.0, np.array([0.01]), 55.0, 1.0, 3.0,
                 0.0, 0.0, 0.0, 0, 7.5, 0, 0.25, 0.0, 0.0, 1.0, 0.0, 0.5,
                 5, 2, 0, 150, 175)
    print(f"  {GREEN}ready{ENDC}\n")

    total_sims = int(params['runs']) * int(params['n_people'])
    n_months   = int(params.get('n_months', 12))
    tpm        = int(params.get('trades_per_month', int(params['num_trades']) // max(1, n_months)))
    print(f"{DIM}Running {total_sims:,} simulations  "
          f"({tpm} trades/month × {n_months} months)...{ENDC}\n")

    from orchestrator import run_parallel, aggregate_results
    raw_results = run_parallel(params, n_jobs=-1, verbose=0)
    print(f"{GREEN}Simulations complete.{ENDC}\n")

    import metrics as M

    print(f"{DIM}Aggregating...{ENDC}", end='', flush=True)
    agg = aggregate_results(raw_results, params)
    print(f"  {GREEN}done{ENDC}")

    print(f"{DIM}Computing drawdown / Sharpe / Sortino / Calmar...{ENDC}", end='', flush=True)
    mdds, sharpes, sortinos, calmars = M.compute_curve_metrics(agg['equity_curves'])
    print(f"  {GREEN}done{ENDC}")

    print(f"{DIM}Computing time under water...{ENDC}", end='', flush=True)
    tuws = M.time_under_water_batch(agg['equity_curves'])
    print(f"  {GREEN}done{ENDC}")

    print(f"{DIM}Computing percentile curves...{ENDC}", end='', flush=True)
    pct = M.percentile_curves(agg['equity_curves'], agg['max_curve_len'])
    print(f"  {GREEN}done{ENDC}")

    print(f"{DIM}Computing monthly breakdown...{ENDC}", end='', flush=True)
    monthly_table, monthly_summary = M.monthly_percentile_table(
        agg['monthly_curves'],
        float(params['account_size']),
        n_months,
        start_year=2027,
    )
    print(f"  {GREEN}done{ENDC}\n")

    portfolio_m = M.portfolio_metrics(agg['final_balances'], params['account_size'])
    dd_m        = M.drawdown_stats(mdds, tuws)
    streak_m    = M.streak_stats(agg['win_streaks'], agg['loss_streaks'], agg['be_streaks'])
    ratio_m     = M.ratio_stats(sharpes, sortinos, calmars)
    rr_m        = M.rr_stats(agg['all_rr'])
    merged_m    = {**portfolio_m, **dd_m, **ratio_m}

    _print_results(agg, params, portfolio_m, dd_m, streak_m, ratio_m, rr_m)

    import plotting as P
    P.plot_equity_curves(pct, agg['equity_curves'], params['account_size'],
                         agg['n_sims'], block=False)
    P.plot_dashboard(
        agg['final_balances'], mdds,
        sharpes, sortinos,
        agg['win_streaks'], agg['loss_streaks'],
        agg['all_rr'], params['account_size'],
        merged_m, block=False,
    )

    # Build header stats from the representative simulation data
    executed  = agg['total_wins'] + agg['total_losses'] + agg['total_be']
    wr_global = (agg['total_wins'] / executed * 100) if executed > 0 else 0.0

    def _header_stats(key):
        s = monthly_summary[key]
        return {
            'Initial balance':   f"${float(params['account_size']):,.0f}",
            'Final balance':     f"${s['final_balance']:,.0f}",
            'Total return':      f"{s['total_return']:+.1f}%",
            'Max drawdown':      f"-{s['max_dd']:.1f}%",
            'Max consec. losses':str(int(streak_m['avg_loss_streak'])),
            'Max consec. wins':  str(int(streak_m['avg_win_streak'])),
            'Win rate':          f'{wr_global:.1f}%',
        }

    extra_stats = {
        'p95': _header_stats('p95'),
        'p50': _header_stats('p50'),
        'p5':  _header_stats('p5'),
    }

    P.plot_monthly_breakdown(monthly_table, float(params['account_size']),
                             extra_stats=extra_stats, block=False)

    end = datetime.now()
    print(f"{DIM}Execution time: {end - start}{ENDC}")
    print(f"{DIM}{end.strftime('%Y-%m-%d  %H:%M:%S')}{ENDC}")

    import matplotlib.pyplot as plt
    plt.show(block=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted.{ENDC}")
        sys.exit(0)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
