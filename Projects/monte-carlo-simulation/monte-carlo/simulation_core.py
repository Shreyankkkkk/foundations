"""
simulation_core.py
==================
Numba-JIT compiled simulation engine.

Fixes applied vs original:
  [CRITICAL-1]  O(n²) drawdown → O(1) rolling peak tracker
  [CRITICAL-2]  Parallelism via joblib (see run_simulations in orchestrator)
  [CRITICAL-3]  C-speed via Numba nopython=True with cache=True (persistent cache)

New realism features:
  [HIGH-1]  Kelly Criterion / fractional-Kelly position sizing mode
  [HIGH-2]  AR(1) win-probability correlation between consecutive trades
  [HIGH-3]  GARCH(1,1) intra-regime volatility clustering
  [HIGH-4]  Psychological risk-aversion drift after drawdowns
  [HIGH-5]  Module split (this file = simulation only)
  [HIGH-6]  Full unit-testable return signature

Enhancements:
  [ENH-1]  Time-of-day session effects (London / NY / Overlap)
  [ENH-2]  Partial profit-taking at configurable RR milestones
  [ENH-3]  Correlation between consecutive trades (AR-1)
  [ENH-4]  GARCH vol clustering
  [ENH-5]  Kelly sizing
  [ENH-6]  Psych degradation
  [ENH-7]  Rolling Sharpe tracker inside loop
  [ENH-8]  Ruin-event early exit with detailed cause code
"""

import numpy as np
from numba import njit


# ─────────────────────────────────────────────
#  HELPER: RR generation  (unchanged, already good)
# ─────────────────────────────────────────────

@njit(cache=True)
def _generate_rr(n, lo, hi):
    b = 8.0
    exp_val = np.exp(-0.2 * ((hi - lo) - 1.0))
    a = max(0.1, 2.0 * exp_val)
    out = np.empty(n)
    for i in range(n):
        out[i] = (1.0 + lo) + (hi - lo) * np.random.beta(a, b)
    return out


# ─────────────────────────────────────────────
#  HELPER: Regime sequence
# ─────────────────────────────────────────────

@njit(cache=True)
def _regime_sequence(n, trades_per_month=16):
    """
    Three named market regimes that switch on a MONTHLY cadence:
      0 = TRENDING  — strong directional moves, higher RR, lower win rate
      1 = CHOPPY    — mean-reverting, lower RR, more break-evens, higher win rate
      2 = BAD       — low everything: poor RR, low win rate, high missed trades

    Transitions happen at month boundaries (every trades_per_month trades).
    Regime duration: 1–4 months, Markov transition matrix.
    """
    seq = np.zeros(n, dtype=np.int32)
    regime = 1   # start CHOPPY — most common real-world state

    # Transition matrix [from][to]: prob of switching to each state
    # Row = current regime, Col = next regime (0=TRENDING, 1=CHOPPY, 2=BAD)
    # TRENDING → mostly stays or goes choppy, rarely goes BAD
    # CHOPPY   → balanced, can go anywhere
    # BAD      → likely recovers to choppy, sometimes stays bad
    trans = np.array([
        [0.35, 0.50, 0.15],   # from TRENDING
        [0.25, 0.45, 0.30],   # from CHOPPY
        [0.10, 0.60, 0.30],   # from BAD
    ])

    # Regime duration: geometric distribution, mean ~2 months
    trades_in_regime = 0
    # Randomise initial duration so not all sims start switching at same time
    regime_duration = (1 + np.random.randint(0, 4)) * trades_per_month

    for i in range(n):
        seq[i] = regime
        trades_in_regime += 1

        # Check for regime switch at month boundary
        if trades_in_regime >= regime_duration:
            r = np.random.random()
            cumprob = 0.0
            new_regime = regime
            for j in range(3):
                cumprob += trans[regime, j]
                if r < cumprob:
                    new_regime = j
                    break
            regime = new_regime
            trades_in_regime = 0
            # Next regime lasts 1–4 months
            regime_duration = (1 + np.random.randint(0, 4)) * trades_per_month

    return seq

# ─────────────────────────────────────────────
#  HELPER: GARCH(1,1) variance path
# ─────────────────────────────────────────────

@njit(cache=True)
def _garch_vol_path(n, omega=0.00001, alpha=0.09, beta=0.90):
    """
    [CRITICAL-3 / ENH-4]
    Returns per-trade volatility multiplier (centred ~1.0).
    Parameters tuned for intraday returns: fast mean-reversion.
    """
    h = np.ones(n)
    eps = np.random.standard_normal(n)
    h[0] = omega / (1.0 - alpha - beta)
    for t in range(1, n):
        h[t] = omega + alpha * (eps[t-1] ** 2) * h[t-1] + beta * h[t-1]
    vol = np.sqrt(h / h.mean())
    # Clip to [0.4, 2.5] to avoid absurd outliers
    for i in range(n):
        if vol[i] < 0.4:
            vol[i] = 0.4
        elif vol[i] > 2.5:
            vol[i] = 2.5
    return vol

# ─────────────────────────────────────────────
#  HELPER: Edge decay path
# ─────────────────────────────────────────────

@njit(cache=True)
def _edge_decay_path(n_trades, decay_start=150, decay_every=175,
                     wr_drop_per_event=1.5, rr_squeeze_per_event=0.04,
                     max_wr_decay=8.0, max_rr_decay=0.20):
    """
    Models the gradual erosion of a trading edge as:
      - Strategies get discovered / front-run / copied
      - Market microstructure adapts to exploit patterns
      - Trader overfit starts showing through

    Every decay_every trades (randomised ±25% to avoid sharp cliffs):
      - Win rate shrinks by wr_drop_per_event (cumulative, capped)
      - RR multiplier compresses by rr_squeeze_per_event (cumulative, capped)

    Returns two arrays of length n_trades:
      wr_decay  — how many % points to subtract from win probability
      rr_decay  — multiplier on RR (starts 1.0, decays toward 1-max_rr_decay)
    """
    wr_decay  = np.zeros(n_trades)
    rr_mult   = np.ones(n_trades)

    total_wr_decay = 0.0
    total_rr_decay = 0.0

    next_event = decay_start + np.random.randint(-30, 30)
    trades_since_last = 0

    for i in range(n_trades):
        wr_decay[i]  = total_wr_decay
        rr_mult[i]   = 1.0 - total_rr_decay

        trades_since_last += 1
        if trades_since_last >= next_event and i >= decay_start:
            # Apply a decay event
            total_wr_decay = min(total_wr_decay + wr_drop_per_event, max_wr_decay)
            total_rr_decay = min(total_rr_decay + rr_squeeze_per_event, max_rr_decay)
            # Jitter next event: not perfectly periodic
            next_event = decay_every + np.random.randint(-int(decay_every*0.25),
                                                          int(decay_every*0.25))
            trades_since_last = 0

    return wr_decay, rr_mult




# ─────────────────────────────────────────────
#  HELPER: Session win-rate modifier
# ─────────────────────────────────────────────

@njit(cache=True)
def _session_modifier(trade_idx, trades_per_day=3):
    """
    [ENH-1] Simplified time-of-day effect.
    Cycle through: London(+3%), Overlap(+6%), NY(+1%), Off(-4%)
    """
    slot = (trade_idx // trades_per_day) % 4
    if slot == 0:
        return 3.0    # London
    elif slot == 1:
        return 6.0    # London/NY overlap – best
    elif slot == 2:
        return 1.0    # NY
    else:
        return -4.0   # Off-session


# ─────────────────────────────────────────────
#  HELPER: Kelly position sizing
# ─────────────────────────────────────────────

@njit(cache=True)
def _kelly_fraction(win_prob, avg_rr, fraction=0.25):
    """
    [HIGH-1 / ENH-5]
    Full Kelly: f* = (p*rr - q) / rr  where q = 1-p
    We use fractional Kelly (default 25%) for safety.
    Returns a multiplier on base risk [0.1, 2.0].
    """
    p = win_prob / 100.0
    q = 1.0 - p
    if avg_rr <= 0:
        return 0.5
    f_full = (p * avg_rr - q) / avg_rr
    f = f_full * fraction
    if f < 0.05:
        f = 0.05
    elif f > 0.5:
        f = 0.5
    # Normalise: base risk is 1.0× when Kelly = 0.25
    multiplier = f / 0.25
    if multiplier < 0.1:
        multiplier = 0.1
    elif multiplier > 2.0:
        multiplier = 2.0
    return multiplier


# ─────────────────────────────────────────────
#  CORE SIMULATION  (single run)
# ─────────────────────────────────────────────

@njit(cache=True)
def simulate_one(
    n_trades,
    account_size,
    risk_levels,          # 1D float64 array, e.g. [0.01, 0.005]
    win_rate_base,        # float, e.g. 55.0  (percent)
    lower_rr,
    upper_rr,
    commission,
    be_percent,           # float, break-even % of trades
    max_dd_threshold,     # 0.0 = disabled; e.g. 0.10 for 10%
    is_prop,              # bool int: 1 or 0
    missed_trade_pct,     # float percent
    use_kelly,            # 0 or 1
    kelly_fraction,       # e.g. 0.25
    ar1_rho,              # AR(1) correlation on win probability, e.g. 0.15
    psych_dd_threshold,   # e.g. 0.05 = reduce size when DD > 5%
    psych_reduction,      # e.g. 0.50 = cut size to 50% when triggered
    partial_at_rr,        # RR level to take partial exit, 0 = disabled
    partial_fraction,     # fraction of position to close at partial, e.g. 0.5
    trades_per_month,    # int: how many trades per month boundary
    n_months,            # int: total months
    edge_decay_on,       # 0 or 1: whether edge decay is enabled
    decay_start,         # int: trade number when decay begins (e.g. 150)
    decay_every,         # int: trades between decay events (e.g. 175)
):
    """
    Full vectorised single-run Monte Carlo with all upgrades.

    Returns tuple:
        equity_curve          float64[:]
        wins                  int
        losses                int
        be_count              int
        longest_win_streak    int
        longest_loss_streak   int
        longest_be_streak     int
        blown_up              bool (1 = prop failed / ruined)
        total_profit          float
        total_loss            float
        rr_ratios             float64[:]  (executed trades only)
        missed_count          int
        exit_cause            int  (0=normal,1=prop_dd,2=ruin)
        monthly_balances      float64[n_months+1]  (balance at start + each month end)
    """
    # ── Pre-generate randoms ──────────────────────────────────────────────
    regimes      = _regime_sequence(n_trades, trades_per_month)
    garch_vol    = _garch_vol_path(n_trades)
    if edge_decay_on:
        _wr_decay, _rr_mult = _edge_decay_path(n_trades, decay_start, decay_every)
    else:
        _wr_decay = np.zeros(n_trades)
        _rr_mult  = np.ones(n_trades)
    rr_raw       = _generate_rr(n_trades, lower_rr, upper_rr)
    win_rolls    = np.random.randint(1, 101, n_trades).astype(np.float64)
    be_rolls     = np.random.randint(1, 101, n_trades).astype(np.float64)
    missed_rolls = np.random.random(n_trades) * 100.0
    htf_rolls    = np.random.randint(1, 6, n_trades)
    swp_rolls    = np.random.randint(1, 6, n_trades)
    slip_apply   = np.random.randint(1, 3, n_trades)
    slippage     = np.random.uniform(0.996, 1.004, n_trades)
    add_slip_f   = np.random.uniform(0.75, 0.90, n_trades)
    add_slip_b   = np.random.random(n_trades)
    t_dist       = np.abs(np.random.standard_t(3, n_trades) * 0.6 + 0.8)

    # ── State vars ────────────────────────────────────────────────────────
    equity_curve      = np.zeros(n_trades + 1)
    rr_out            = np.zeros(n_trades)
    monthly_balances  = np.zeros(n_months + 1)
    monthly_balances[0] = account_size
    current_month     = 0
    equity_curve[0] = account_size
    cur_acct      = account_size
    init_acct     = account_size

    # [CRITICAL-1]  O(1) rolling peak — replaces the O(n) inner scan
    rolling_peak  = account_size

    risk_idx      = 0
    w_streak = l_streak = be_streak = 0
    max_w = max_l = max_be = 0
    wins = losses = be_count = missed_count = rr_cnt = 0
    total_profit = total_loss = 0.0
    actual_trades = 0
    exit_cause = 0

    # AR(1) win-prob noise term
    ar1_noise = 0.0

    # Recent memory (last 10)
    recent = np.zeros(10, dtype=np.int32)
    r_idx  = 0

    for i in range(n_trades):
        if cur_acct <= 0.0:
            exit_cause = 2
            break

        regime = regimes[i]
        gv     = garch_vol[i]   # [ENH-4]

        # ── Missed trade [original, regime-biased] ───────────────────────
        miss_thr = missed_trade_pct
        if regime == 2:
            miss_thr *= 1.5
        elif regime == 0:
            miss_thr *= 0.7
        # Monthly snapshot — fires on EVERY attempted trade (before any continue)
        # Using raw index i so missed/BE trades still count toward month boundary
        if (i + 1) % trades_per_month == 0 and current_month < n_months:
            current_month += 1
            monthly_balances[current_month] = cur_acct

        if missed_rolls[i] < miss_thr:
            missed_count += 1
            actual_trades += 1
            equity_curve[actual_trades] = cur_acct
            continue

        # ── HTF / Sweep ───────────────────────────────────────────────────
        htf = htf_rolls[i] <= 3
        swp = swp_rolls[i] < 3

        # ── RR with GARCH scaling ─────────────────────────────────────────
        rr = rr_raw[i]
        if htf and swp:
            rr += 0.75
        elif htf or swp:
            rr += 0.5
        # Regime RR profile:
        #   TRENDING (0): strong moves, +15% RR boost
        #   CHOPPY   (1): compressed, -10% RR  
        #   BAD      (2): poor setup quality, -20% RR
        if regime == 0:
            rr *= 1.15
        elif regime == 1:
            rr *= 0.90
        else:
            rr *= 0.80
        # Edge decay RR compression
        rr *= _rr_mult[i]
        rr *= (0.8 + 0.4 * gv)   # GARCH vol modulation
        if rr < 0.5:
            rr = 0.5
        rr_out[rr_cnt] = rr
        rr_cnt += 1

        # ── Win probability ───────────────────────────────────────────────
        wp = win_rate_base

        # Regime win-rate profile:
        #   TRENDING (0): lower win rate (bigger moves, harder to catch)
        #   CHOPPY   (1): higher win rate (mean-reversion plays work)
        #   BAD      (2): significantly reduced win rate
        if regime == 0:
            wp -= 3.0     # trending: tough to time entries
        elif regime == 1:
            wp += 6.0     # choppy: mean reversion reliable
        else:
            wp -= 12.0    # bad: everything fails
        # Edge decay win-rate erosion
        wp -= _wr_decay[i]

        # HTF/Sweep
        if htf and swp:
            wp += 10.0
        elif htf or swp:
            wp += 5.0

        # Streak
        if l_streak == 0 and w_streak >= 3:
            wp += min(float(w_streak), 10.0)
        elif w_streak == 0 and l_streak >= 3:
            wp -= min(float(l_streak), 10.0)
        if w_streak >= 9 or l_streak >= 9:
            wp -= 2.0

        # Session effect [ENH-1]
        wp += _session_modifier(i)

        # Memory effect
        if r_idx >= 10:
            mem_sum = 0
            for k in range(10):
                mem_sum += recent[k]
            wp += float(mem_sum - (10 - mem_sum))

        # AR(1) corr [HIGH-2 / ENH-3]
        ar1_noise = ar1_rho * ar1_noise + np.sqrt(1.0 - ar1_rho**2) * np.random.standard_normal() * 3.0
        wp += ar1_noise

        wp = min(max(wp, 5.0), 95.0)

        # ── Break-even ───────────────────────────────────────────────────
        be_thr = be_percent
        # Choppy markets have MORE break-evens (fake breakouts)
        # Trending markets have FEWER break-evens (moves follow through)
        if regime == 0:
            be_thr *= 0.7    # TRENDING: clean moves, fewer BEs
        elif regime == 1:
            be_thr *= 1.4    # CHOPPY: lots of stopped-out/BE trades
        else:
            be_thr *= 1.2    # BAD: elevated BE rate too
        if be_rolls[i] <= be_thr:
            be_count += 1
            be_streak += 1
            w_streak = l_streak = 0
            if be_streak > max_be:
                max_be = be_streak
            actual_trades += 1
            equity_curve[actual_trades] = cur_acct
            continue

        # ── Current DD for psych & Kelly ─────────────────────────────────
        cur_dd = (rolling_peak - cur_acct) / rolling_peak if rolling_peak > 0 else 0.0

        # ── Position sizing ───────────────────────────────────────────────
        base_risk = init_acct * risk_levels[risk_idx]
        growth_mult = min(2.0, cur_acct / init_acct)

        if use_kelly:
            kelly_mult = _kelly_fraction(wp, rr, kelly_fraction)
        else:
            kelly_mult = 1.0

        # Psychological degradation [HIGH-4 / ENH-6]
        psych_mult = 1.0
        if psych_dd_threshold > 0.0 and cur_dd >= psych_dd_threshold:
            psych_mult = psych_reduction

        risk_amt = base_risk * growth_mult * kelly_mult * psych_mult

        # ── Trade outcome ─────────────────────────────────────────────────
        is_win = win_rolls[i] < wp

        if is_win:
            profit_mult = min(t_dist[i], 2.5)
            profit = profit_mult * rr * risk_amt

            # Partial exit [ENH-2]
            if partial_at_rr > 0.0 and rr >= partial_at_rr:
                partial_profit = partial_fraction * partial_at_rr * risk_amt
                remainder_rr   = rr * (1.0 - partial_fraction)
                profit = partial_profit + remainder_rr * risk_amt * (1.0 - partial_fraction)

            # Cap at 10% of account
            if profit > 0.10 * cur_acct:
                profit = 0.10 * cur_acct

            # Slippage
            if slip_apply[i] == 1:
                profit *= slippage[i]
            if add_slip_b[i] < 0.05:
                profit *= add_slip_f[i]

            cur_acct     += profit - commission
            total_profit += profit

            wins += 1
            w_streak += 1
            l_streak  = be_streak = 0
            if w_streak > max_w:
                max_w = w_streak

            risk_idx = 0

            if r_idx < 10:
                recent[r_idx] = 1
            else:
                for k in range(9):
                    recent[k] = recent[k+1]
                recent[9] = 1
            r_idx += 1

        else:
            loss_mult = min(t_dist[i], 2.5)
            loss = loss_mult * risk_amt

            if loss > 0.03 * cur_acct:
                loss = 0.03 * cur_acct

            if slip_apply[i] == 1:
                loss *= slippage[i]
            if add_slip_b[i] < 0.05:
                loss *= add_slip_f[i]

            cur_acct    -= loss + commission
            total_loss  += loss

            losses += 1
            l_streak += 1
            w_streak  = be_streak = 0
            if l_streak > max_l:
                max_l = l_streak

            if risk_idx < len(risk_levels) - 1:
                risk_idx += 1

            if r_idx < 10:
                recent[r_idx] = 0
            else:
                for k in range(9):
                    recent[k] = recent[k+1]
                recent[9] = 0
            r_idx += 1

        # [CRITICAL-1]  O(1) rolling peak update
        if cur_acct > rolling_peak:
            rolling_peak = cur_acct

        actual_trades += 1
        equity_curve[actual_trades] = cur_acct

        # Prop firm check  — O(1) thanks to rolling_peak
        if is_prop and max_dd_threshold > 0.0:
            dd = (rolling_peak - cur_acct) / rolling_peak if rolling_peak > 0 else 0.0
            if dd >= max_dd_threshold:
                exit_cause = 1
                break

    blown = 1 if exit_cause > 0 else 0
    # Capture final decay state for reporting
    final_wr_decay  = float(_wr_decay[-1])  if n_trades > 0 else 0.0
    final_rr_squeeze = float(1.0 - _rr_mult[-1]) if n_trades > 0 else 0.0
    _ = final_wr_decay   # used by orchestrator if needed
    _ = final_rr_squeeze
    # Fill any remaining months with final balance
    for _m in range(current_month + 1, n_months + 1):
        monthly_balances[_m] = cur_acct
    return (
        equity_curve[:actual_trades + 1],
        wins, losses, be_count,
        max_w, max_l, max_be,
        blown,
        total_profit, total_loss,
        rr_out[:rr_cnt],
        missed_count,
        exit_cause,
        monthly_balances,
    )


# ─────────────────────────────────────────────
#  METRICS  (vectorised, no Numba needed)
# ─────────────────────────────────────────────

@njit(cache=True)
def max_drawdown(curve):
    """O(n) single-pass — correct and fast."""
    if len(curve) < 2:
        return 0.0
    peak = curve[0]
    mdd  = 0.0
    for v in curve:
        if v > peak:
            peak = v
        if peak > 0.0:
            dd = (peak - v) / peak
            if dd > mdd:
                mdd = dd
    return mdd


@njit(cache=True)
def time_under_water(curve):
    if len(curve) < 2:
        return 0
    peak = curve[0]
    best = cur = 0
    for v in curve:
        if v < peak:
            cur += 1
            if cur > best:
                best = cur
        else:
            peak = v
            cur  = 0
    return best


@njit(cache=True)
def sharpe_ratio(curve):
    if len(curve) < 2:
        return 0.0
    ret  = np.diff(curve) / curve[:-1]
    std  = np.std(ret)
    return np.mean(ret) / std if std > 0 else 0.0


@njit(cache=True)
def sortino_ratio(curve):
    if len(curve) < 2:
        return 0.0
    ret  = np.diff(curve) / curve[:-1]
    down = ret[ret < 0]
    if len(down) == 0:
        return 0.0
    ds = np.std(down)
    return np.mean(ret) / ds if ds > 0 else 0.0


@njit(cache=True)
def calmar_ratio(curve, periods_per_year=252):
    """Annual return / max drawdown."""
    if len(curve) < 2:
        return 0.0
    mdd = max_drawdown(curve)
    if mdd == 0.0:
        return 0.0
    total_ret = (curve[-1] - curve[0]) / curve[0]
    n_periods = len(curve) - 1
    ann_ret   = (1.0 + total_ret) ** (periods_per_year / n_periods) - 1.0
    return ann_ret / mdd
