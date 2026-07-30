"""
metrics.py  —  fast vectorised analytics
"""

import numpy as np
from collections import Counter
import math


# ── Monthly analytics ─────────────────────────────────────────────────────────

def monthly_percentile_table(monthly_curves, account_size, n_months, start_year=2027):
    """
    Find the single representative simulation closest to P5, P50, P95 final balance.
    Then read that simulation's actual month-by-month journey.

    This guarantees:
      - Monthly % values are real month-over-month returns from ONE coherent path
      - Monthly $ values compound correctly (based on actual running balance)
      - Monthly %s sum (compound) to the year total correctly
      - No cross-sectional percentile mixing

    Returns list of year dicts, each with:
      months: list of {name, p5_pct, p5_usd, p50_pct, p50_usd, p95_pct, p95_usd}
      total:  {p5_pct, p5_usd, p50_pct, p50_usd, p95_pct, p95_usd}
    Also returns summary stats per scenario as a second return value.
    """
    MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun',
                   'Jul','Aug','Sep','Oct','Nov','Dec']

    mat = np.array([c for c in monthly_curves], dtype=np.float64)  # (n_sims, n_months+1)
    final_bals = mat[:, n_months]

    # Find representative sim for each percentile
    def _rep_idx(pct):
        target = np.percentile(final_bals, pct)
        return int(np.argmin(np.abs(final_bals - target)))

    rep = {
        'p95': _rep_idx(95),
        'p50': _rep_idx(50),
        'p5':  _rep_idx(5),
    }

    # Build per-sim monthly returns
    def _monthly_data(sim_idx):
        """Extract month-by-month % and $ from one simulation's actual curve."""
        curve = mat[sim_idx]   # shape (n_months+1,)
        months_data = []
        for m in range(n_months):
            prev = float(curve[m])
            curr = float(curve[m + 1])
            pct  = round((curr - prev) / prev * 100.0, 1) if prev > 0 else 0.0
            usd  = round(curr - prev, 0)
            months_data.append((pct, usd, curr))
        return months_data

    data = {k: _monthly_data(v) for k, v in rep.items()}

    # Organise into year dicts
    results    = []
    year       = start_year
    month_idx  = 0

    while month_idx < n_months:
        year_data        = {'year': year, 'months': []}
        months_this_year = min(12, n_months - month_idx)

        for m in range(months_this_year):
            mi = month_idx + m
            row = {
                'name':    MONTH_NAMES[mi % 12],
                'p5_pct':  data['p5'][mi][0],
                'p5_usd':  data['p5'][mi][1],
                'p5_bal':  data['p5'][mi][2],
                'p50_pct': data['p50'][mi][0],
                'p50_usd': data['p50'][mi][1],
                'p50_bal': data['p50'][mi][2],
                'p95_pct': data['p95'][mi][0],
                'p95_usd': data['p95'][mi][1],
                'p95_bal': data['p95'][mi][2],
            }
            year_data['months'].append(row)

        # Year total: compound return from start to end of this year
        yr_end   = month_idx + months_this_year
        yr_start = month_idx

        def _yr_total(key):
            start_bal = float(mat[rep[key], yr_start])
            end_bal   = float(mat[rep[key], yr_end])
            pct = round((end_bal - start_bal) / start_bal * 100.0, 1) if start_bal > 0 else 0.0
            usd = round(end_bal - start_bal, 0)
            return pct, usd

        p5_t  = _yr_total('p5')
        p50_t = _yr_total('p50')
        p95_t = _yr_total('p95')

        year_data['total'] = {
            'p5_pct':  p5_t[0],  'p5_usd':  p5_t[1],  'p5_bal':  float(mat[rep['p5'],  yr_end]),
            'p50_pct': p50_t[0], 'p50_usd': p50_t[1], 'p50_bal': float(mat[rep['p50'], yr_end]),
            'p95_pct': p95_t[0], 'p95_usd': p95_t[1], 'p95_bal': float(mat[rep['p95'], yr_end]),
        }

        results.append(year_data)
        month_idx += months_this_year
        year      += 1

    # Build summary stats (final balance, total return, etc.)
    def _summary(key):
        idx       = rep[key]
        final_b   = float(mat[idx, n_months])
        total_ret = round((final_b / float(account_size) - 1.0) * 100.0, 1)
        # Max drawdown for this sim
        curve = mat[idx]
        peak  = curve[0]; mdd = 0.0
        for v in curve:
            if v > peak: peak = v
            if peak > 0:
                dd = (peak - v) / peak
                if dd > mdd: mdd = dd
        # Estimate max consecutive from overall agg (not per-sim here — use placeholder)
        return {
            'final_balance': round(final_b, 0),
            'total_return':  total_ret,
            'max_dd':        round(mdd * 100.0, 1),
        }

    summary = {k: _summary(k) for k in ('p95', 'p50', 'p5')}

    return results, summary


def percentile_curves(all_curves, max_len, sample_n=5000,
                      percentiles=(0, 5, 25, 50, 75, 95, 100)):
    n = len(all_curves)
    sample_n = min(sample_n, n)
    idx = np.random.choice(n, sample_n, replace=False)
    sampled = [all_curves[i] for i in idx]

    mat = np.full((sample_n, max_len), np.nan, dtype=np.float32)
    for i, c in enumerate(sampled):
        mat[i, :len(c)] = c

    return {p: np.nanpercentile(mat, p, axis=0) for p in percentiles}


# ── Per-curve metrics in vectorised chunks ────────────────────────────────────

def compute_curve_metrics(all_curves, chunk_size=10_000):
    n = len(all_curves)
    mdds     = np.empty(n, dtype=np.float64)
    sharpes  = np.empty(n, dtype=np.float64)
    sortinos = np.empty(n, dtype=np.float64)
    calmars  = np.empty(n, dtype=np.float64)

    for start in range(0, n, chunk_size):
        batch = all_curves[start:start + chunk_size]
        b     = len(batch)
        blen  = max(len(c) for c in batch)

        m = np.full((b, blen), np.nan, dtype=np.float32)
        for i, c in enumerate(batch):
            m[i, :len(c)] = c

        filled = np.where(np.isnan(m), -np.inf, m)
        rmax   = np.maximum.accumulate(filled, axis=1).astype(np.float32)
        rmax[rmax == -np.inf] = np.nan
        with np.errstate(invalid='ignore', divide='ignore'):
            dd = np.where(rmax > 0, (rmax - m) / rmax, 0.0)
        dd = np.nan_to_num(dd, nan=0.0)
        mdds[start:start + b] = dd.max(axis=1)

        m0 = m[:, :-1].astype(np.float64)
        m1 = m[:, 1:].astype(np.float64)
        with np.errstate(invalid='ignore', divide='ignore'):
            rets = np.where(
                (~np.isnan(m0)) & (~np.isnan(m1)) & (m0 != 0),
                (m1 - m0) / m0, np.nan)

        mean_r = np.nanmean(rets, axis=1)
        std_r  = np.nanstd(rets, axis=1)
        sharpes[start:start + b] = np.where(std_r > 0, mean_r / std_r, 0.0)

        down_r = np.where(rets < 0, rets, np.nan)
        down_s = np.nanstd(down_r, axis=1)
        sortinos[start:start + b] = np.where(down_s > 0, mean_r / down_s, 0.0)

        first = np.array([float(c[0])  for c in batch])
        last  = np.array([float(c[-1]) for c in batch])
        lens  = np.array([len(c)       for c in batch], dtype=np.float64)
        with np.errstate(invalid='ignore', divide='ignore'):
            total_ret = np.where(first > 0, (last - first) / first, 0.0)
            ann_ret   = np.where(lens > 1,
                                 (1.0 + total_ret) ** (252.0 / lens) - 1.0, 0.0)
        batch_mdd = mdds[start:start + b]
        calmars[start:start + b] = np.where(batch_mdd > 0, ann_ret / batch_mdd, 0.0)

    return mdds, sharpes, sortinos, calmars


def time_under_water_batch(all_curves, chunk_size=10_000):
    n    = len(all_curves)
    tuws = np.empty(n, dtype=np.int32)

    for start in range(0, n, chunk_size):
        batch = all_curves[start:start + chunk_size]
        b     = len(batch)
        blen  = max(len(c) for c in batch)

        m = np.full((b, blen), np.nan, dtype=np.float32)
        for i, c in enumerate(batch):
            m[i, :len(c)] = c

        filled     = np.where(np.isnan(m), -np.inf, m)
        rmax       = np.maximum.accumulate(filled, axis=1).astype(np.float32)
        rmax[rmax == -np.inf] = np.nan
        underwater = (m < rmax).astype(np.int32)

        for i in range(b):
            row  = underwater[i]
            best = cur = 0
            for v in row:
                if v:
                    cur += 1
                    best = max(best, cur)
                else:
                    cur = 0
            tuws[start + i] = best

    return tuws


# ── Summary statistics ────────────────────────────────────────────────────────

def portfolio_metrics(final_balances, account_size):
    account_size = float(account_size)
    fb  = np.asarray(final_balances, dtype=np.float64)
    ret = (fb / account_size) - 1.0
    var5 = np.percentile(ret, 5)
    es   = float(ret[ret <= var5].mean()) if np.any(ret <= var5) else float(var5)
    return {
        "var_5":               round(float(var5), 4),
        "expected_shortfall":  round(es, 4),
        "prob_ruin":           round(float(np.mean(fb < 0.5 * account_size)) * 100, 2),
        "prob_double":         round(float(np.mean(fb >= 2.0 * account_size)) * 100, 2),
        "prob_profit":         round(float(np.mean(fb > account_size)) * 100, 2),
        "max_final":           round(float(fb.max()), 2),
        "min_final":           round(float(fb.min()), 2),
        "mean_final":          round(float(fb.mean()), 2),
        "median_final":        round(float(np.median(fb)), 2),
        "std_final":           round(float(fb.std()), 2),
    }


def rr_stats(rr_array):
    rr = np.asarray(rr_array)
    if len(rr) == 0:
        return {}
    c = Counter(np.round(rr, 1))
    most_common, _ = c.most_common(1)[0]
    return {
        "mean":        round(float(rr.mean()), 3),
        "median":      round(float(np.median(rr)), 3),
        "p5":          round(float(np.percentile(rr, 5)), 3),
        "p95":         round(float(np.percentile(rr, 95)), 3),
        "min":         round(float(rr.min()), 3),
        "max":         round(float(rr.max()), 3),
        "most_common": round(float(most_common), 1),
    }


def streak_stats(win_streaks, loss_streaks, be_streaks):
    return {
        "avg_win_streak":  round(float(np.mean(win_streaks)), 2),
        "max_win_streak":  int(np.max(win_streaks)),
        "avg_loss_streak": round(float(np.mean(loss_streaks)), 2),
        "max_loss_streak": int(np.max(loss_streaks)),
        "avg_be_streak":   round(float(np.mean(be_streaks)), 2),
        "max_be_streak":   int(np.max(be_streaks)),
    }


def drawdown_stats(mdd_array, tuw_array):
    mdd = np.asarray(mdd_array)
    tuw = np.asarray(tuw_array)
    return {
        "avg_mdd_pct":    round(float(mdd.mean()) * 100, 2),
        "worst_mdd_pct":  round(float(mdd.max()) * 100, 2),
        "p95_mdd_pct":    round(float(np.percentile(mdd, 95)) * 100, 2),
        "avg_tuw_trades": round(float(tuw.mean()), 1),
        "worst_tuw":      int(tuw.max()),
    }


def ratio_stats(sharpes, sortinos, calmars):
    return {
        "avg_sharpe":  round(float(np.mean(sharpes)), 3),
        "avg_sortino": round(float(np.mean(sortinos)), 3),
        "avg_calmar":  round(float(np.mean(calmars)), 3),
    }
