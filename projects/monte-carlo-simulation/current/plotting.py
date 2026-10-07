"""
plotting.py
===========
Professional dark-theme visualisation suite.
All charts use a consistent design system:
  - Dark background (#0d0d0d)
  - Accent palette: cyan, lime, amber, coral
  - Thin grid lines, clean typography
  - Minimal chrome — data first
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
from scipy.stats import gaussian_kde
from collections import Counter


# ─────────────────────────────────────────────────────────────
#  DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────

BG       = "#141414"   # warm charcoal — matches Chart 4
BG2      = "#1a1a1a"
GRID     = "#2a2a2a"
TEXT_PRI = "#f0f0f0"
TEXT_SEC = "#7a7a7a"

LIME    = "#34d399"   # emerald — matches Chart 4 positive
CYAN    = "#38bdf8"   # sky blue
AMBER   = "#fbbf24"   # warm amber
CORAL   = "#f87171"   # soft red — matches Chart 4 negative
PURPLE  = "#a78bfa"   # lavender
WHITE   = "#f5f5f5"

PALETTE = [CYAN, LIME, AMBER, CORAL, PURPLE, "#2dd4bf", "#fb923c"]


def _apply_dark(fig, axes):
    """Apply dark theme to a fig + list of axes."""
    fig.patch.set_facecolor(BG)
    for ax in axes:
        ax.set_facecolor(BG2)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        ax.xaxis.label.set_color(TEXT_SEC)
        ax.yaxis.label.set_color(TEXT_SEC)
        ax.title.set_color(TEXT_PRI)
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID)
        ax.grid(True, color=GRID, linewidth=0.4, alpha=0.6)


def _dollar_fmt(x, _):
    if abs(x) >= 1e6:
        return f"${x/1e6:.1f}M"
    if abs(x) >= 1e3:
        return f"${x/1e3:.0f}K"
    return f"${x:.0f}"


def _pct_fmt(x, _):
    return f"{x:.1f}%"


# ─────────────────────────────────────────────────────────────
#  CHART 1 — Equity Curves (percentile fan)
# ─────────────────────────────────────────────────────────────

def plot_equity_curves(pct_curves, all_equity_curves, account_size,
                       n_sims, block=False):
    """
    Percentile-fan equity curve.
    pct_curves: dict from metrics.percentile_curves()
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    _apply_dark(fig, [ax])

    # Ghost sample — max 80 curves for readability
    n_ghost = min(80, len(all_equity_curves))
    idx     = np.random.choice(len(all_equity_curves), n_ghost, replace=False)
    for i in idx:
        ax.plot(all_equity_curves[i], color=WHITE, alpha=0.025, linewidth=0.4)

    x = range(len(pct_curves[50]))

    # Shaded bands
    ax.fill_between(x, pct_curves[0],  pct_curves[5],
                    color=CORAL,  alpha=0.12, label="0 – 5th %ile")
    ax.fill_between(x, pct_curves[5],  pct_curves[25],
                    color=AMBER,  alpha=0.10, label="5 – 25th %ile")
    ax.fill_between(x, pct_curves[25], pct_curves[75],
                    color=LIME,   alpha=0.10, label="25 – 75th %ile")
    ax.fill_between(x, pct_curves[75], pct_curves[95],
                    color=AMBER,  alpha=0.10, label="75 – 95th %ile")
    ax.fill_between(x, pct_curves[95], pct_curves[100],
                    color=CYAN,   alpha=0.12, label="95 – 100th %ile")

    # Key lines
    ax.plot(pct_curves[50],  color=LIME,   linewidth=2.2, label="Median (P50)", zorder=5)
    ax.plot(pct_curves[5],   color=CORAL,  linewidth=1.6, linestyle="--", label="P5", zorder=5)
    ax.plot(pct_curves[95],  color=CYAN,   linewidth=1.6, linestyle="--", label="P95", zorder=5)

    # Starting line
    ax.axhline(account_size, color=TEXT_SEC, linestyle=":", linewidth=0.8, alpha=0.6)

    ax.yaxis.set_major_formatter(FuncFormatter(_dollar_fmt))
    ax.set_xlabel("Trade Number", fontsize=10)
    ax.set_ylabel("Account Balance", fontsize=10)
    ax.set_title(f"Monte Carlo Equity Curves — {n_sims:,} Simulations", fontsize=13, pad=14)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.2, labelcolor=TEXT_SEC)

    fig.tight_layout()
    plt.show(block=block)
    return fig


# ─────────────────────────────────────────────────────────────
#  CHART 2 — Dashboard  (6-panel)
# ─────────────────────────────────────────────────────────────

def plot_dashboard(final_balances, max_dds, sharpes, sortinos,
                   win_streaks, loss_streaks, rr_ratios, account_size,
                   metrics_dict, block=False):
    """
    6-panel summary dashboard in a professional dark layout.
    """
    fig = plt.figure(figsize=(16, 10))
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.32)

    axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(3)]
    _apply_dark(fig, axes)
    fig.patch.set_facecolor(BG)

    fb  = np.array(final_balances)
    mdd = np.array(max_dds) * 100

    # ── Panel 0: Final balance distribution ──────────────────────────────
    ax = axes[0]
    ax.set_title("Final Balance Distribution", fontsize=11)
    n_bins = min(120, max(30, len(fb) // 20))
    ax.hist(fb, bins=n_bins, color=LIME, alpha=0.75, edgecolor="none")
    ax.axvline(account_size,       color=WHITE,  linewidth=1.0, linestyle=":",  alpha=0.5, label="Start")
    ax.axvline(fb.mean(),          color=AMBER,  linewidth=1.4, linestyle="--", label=f"Mean ${fb.mean():,.0f}")
    ax.axvline(np.median(fb),      color=CYAN,   linewidth=1.4, linestyle="--", label=f"Median ${np.median(fb):,.0f}")
    ax.xaxis.set_major_formatter(FuncFormatter(_dollar_fmt))
    ax.set_ylabel("Frequency", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.2, labelcolor=TEXT_SEC)

    # ── Panel 1: Drawdown distribution ───────────────────────────────────
    ax = axes[1]
    ax.set_title("Max Drawdown Distribution", fontsize=11)
    ax.hist(mdd, bins=60, color=CORAL, alpha=0.75, edgecolor="none")
    ax.axvline(mdd.mean(), color=AMBER, linewidth=1.4, linestyle="--",
               label=f"Mean {mdd.mean():.1f}%")
    ax.xaxis.set_major_formatter(FuncFormatter(_pct_fmt))
    ax.set_ylabel("Frequency", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.2, labelcolor=TEXT_SEC)

    # ── Panel 2: RR distribution (KDE) ───────────────────────────────────
    ax = axes[2]
    ax.set_title("Risk : Reward Distribution", fontsize=11)
    rr = np.asarray(rr_ratios)
    if len(rr) > 10:
        sample = rr if len(rr) <= 500_000 else np.random.choice(rr, 500_000, replace=False)
        kde = gaussian_kde(sample)
        xs  = np.linspace(rr.min(), rr.max(), 800)
        ys  = kde(xs)
        ax.plot(xs, ys, color=PURPLE, linewidth=1.8)
        ax.fill_between(xs, ys, alpha=0.2, color=PURPLE)
        ax.axvline(rr.mean(),   color=AMBER, linewidth=1.2, linestyle="--",
                   label=f"Mean {rr.mean():.2f}")
        ax.axvline(np.median(rr), color=CYAN, linewidth=1.2, linestyle="--",
                   label=f"Median {np.median(rr):.2f}")
    ax.set_xlabel("RR Ratio", fontsize=9)
    ax.set_ylabel("Density", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.2, labelcolor=TEXT_SEC)

    # ── Panel 3: Sharpe vs Sortino scatter ───────────────────────────────
    ax = axes[3]
    ax.set_title("Sharpe vs Sortino", fontsize=11)
    ax.scatter(sharpes, sortinos, color=CYAN, alpha=0.25, s=4, edgecolors="none")
    ax.set_xlabel("Sharpe Ratio", fontsize=9)
    ax.set_ylabel("Sortino Ratio", fontsize=9)
    ax.axhline(0, color=GRID, linewidth=0.8)
    ax.axvline(0, color=GRID, linewidth=0.8)

    # ── Panel 4: Streak comparison ────────────────────────────────────────
    ax = axes[4]
    ax.set_title("Streak Distribution", fontsize=11)
    ws = np.array(win_streaks)
    ls = np.array(loss_streaks)
    top = max(ws.max(), ls.max()) + 1
    bins = np.arange(0, top + 1, 1)
    ax.hist(ws, bins=bins, color=LIME,  alpha=0.6, label="Win streaks",  edgecolor="none")
    ax.hist(ls, bins=bins, color=CORAL, alpha=0.6, label="Loss streaks", edgecolor="none")
    ax.set_xlabel("Streak Length", fontsize=9)
    ax.set_ylabel("Frequency", fontsize=9)
    ax.legend(fontsize=7, framealpha=0.2, labelcolor=TEXT_SEC)

    # ── Panel 5: Key metrics text card ───────────────────────────────────
    ax = axes[5]
    ax.set_title("Risk Summary", fontsize=11)
    ax.axis("off")

    m = metrics_dict
    lines = [
        ("5% VaR",              f"{m['var_5']:.3f}",           CORAL),
        ("Expected Shortfall",  f"{m['expected_shortfall']:.3f}", CORAL),
        ("Prob of Ruin <50%",   f"{m['prob_ruin']:.1f}%",       CORAL),
        ("Prob of Profit",      f"{m['prob_profit']:.1f}%",      LIME),
        ("Prob of 2× Account",  f"{m['prob_double']:.1f}%",      LIME),
        ("Avg Max Drawdown",    f"{m.get('avg_mdd_pct',0):.1f}%", AMBER),
        ("Worst Drawdown",      f"{m.get('worst_mdd_pct',0):.1f}%", CORAL),
        ("Avg Sharpe",          f"{m.get('avg_sharpe',0):.3f}",  CYAN),
        ("Avg Sortino",         f"{m.get('avg_sortino',0):.3f}", CYAN),
        ("Avg Calmar",          f"{m.get('avg_calmar',0):.3f}",  CYAN),
    ]
    for j, (label, val, colour) in enumerate(lines):
        y = 0.94 - j * 0.095
        ax.text(0.02, y, label,  transform=ax.transAxes,
                fontsize=9, color=TEXT_SEC, va="top")
        ax.text(0.98, y, val,   transform=ax.transAxes,
                fontsize=9, color=colour,   va="top", ha="right", fontweight="bold")

    fig.suptitle("Monte Carlo — Performance Dashboard", fontsize=14,
                 color=TEXT_PRI, y=0.995, fontweight="bold")
    plt.show(block=block)
    return fig


# ─────────────────────────────────────────────────────────────
#  CHART 3 — Regime analysis
# ─────────────────────────────────────────────────────────────

def plot_regime_waterfall(pct_curves, account_size, block=False):
    """Return distribution at key trade milestones."""
    curve  = pct_curves[50]
    length = len(curve)
    if length < 4:
        return None

    checkpoints = [int(length * f) for f in (0.25, 0.5, 0.75, 1.0)]
    labels       = ["25% through", "Halfway", "75%", "Final"]

    fig, ax = plt.subplots(figsize=(10, 5))
    _apply_dark(fig, [ax])

    for cp, lbl, col in zip(checkpoints, labels, PALETTE):
        ax.axvline(cp, color=col, linewidth=1.0, linestyle="--", alpha=0.5)
        ax.text(cp + 2, ax.get_ylim()[1] if ax.get_ylim()[1] != 1.0 else 0.9,
                lbl, color=col, fontsize=8)

    ax.plot(curve, color=LIME, linewidth=2)
    ax.axhline(account_size, color=TEXT_SEC, linewidth=0.6, linestyle=":")
    ax.yaxis.set_major_formatter(FuncFormatter(_dollar_fmt))
    ax.set_xlabel("Trade Number", fontsize=10)
    ax.set_ylabel("Median Balance", fontsize=10)
    ax.set_title("Median Equity Path with Checkpoints", fontsize=12)
    fig.tight_layout()
    plt.show(block=block)
    return fig




# ─────────────────────────────────────────────────────────────
#  CHART 4 — Monthly breakdown  (one figure per scenario)
#
#  Design:
#    • Dark navy base  #0a0e1a
#    • Scenario accent colour used only for headers and total row
#    • Alternating subtle row shading for readability
#    • 4 columns: Month | % | $ gain | Balance
#    • Year total row shows: year % | year $ | running balance
#    • Cumulative return shown in total row subtitle
#    • Max 3 year-tables per row, wrapping cleanly
#    • One figure per scenario (P95 / P50 / P5) — 3 windows total
# ─────────────────────────────────────────────────────────────

# ── Colour palette ────────────────────────────────────────────
# ── Palette: warm charcoal base, mineral accents ─────────────
# Background family — warm charcoal, not cold navy
_BG_FIG    = '#141414'   # near-black warm charcoal
_BG_HEADER = '#1a1a1a'   # header strip
_BG_COL_HDR= '#1f1f1f'   # column label row
_BG_ROW_A  = '#161616'   # alternating row A (slightly lighter)
_BG_ROW_B  = '#131313'   # alternating row B
_BORDER    = '#2a2a2a'   # subtle warm-grey border

# Typography
_TXT_HEAD  = '#f5f5f5'   # near-white for headers
_TXT_COL   = '#6b6b6b'   # dim grey for column labels
_TXT_MONTH = '#9a9a9a'   # medium grey for month names
_TXT_NEUT  = '#d4d4d4'   # light grey for balance column
_TXT_POS   = '#34d399'   # emerald green — profit
_TXT_NEG   = '#f87171'   # soft red — loss  (unchanged)
_TXT_ZERO  = '#4b4b4b'   # very dim for zero values

# Scenario accents — each tells a story through its colour
#   P95 Best:    Rich amber-gold   — wealth, achievement
#   P50 Median:  Indigo-purple     — balanced, measured
#   P5  Worst:   Muted coral-red   — caution, risk
_S_META = [
    # label,                 pct_key,   usd_key,   bal_key,
    # accent (pill/header),  dark tint (total row bg), stat_key
    ('P95  —  Best case',
     'p95_pct', 'p95_usd', 'p95_bal',
     '#d97706', '#2d1f04', 'p95'),   # amber

    ('P50  —  Median case',
     'p50_pct', 'p50_usd', 'p50_bal',
     '#7c3aed', '#1e0f3d', 'p50'),   # violet

    ('P5  —  Worst case',
     'p5_pct',  'p5_usd',  'p5_bal',
     '#dc2626', '#2d0a0a', 'p5'),    # deep red
]


def _val_colour(v):
    if   v > 0.05:  return _TXT_POS
    elif v < -0.05: return _TXT_NEG
    else:           return _TXT_ZERO


def _fmt_pct(v):
    return f'{v:+.1f}%'


def _fmt_money(v, compact=True):
    """Format dollar value. compact=True → $1.2k style."""
    neg = v < 0
    av  = abs(v)
    if compact:
        if av >= 1_000_000: s = f'${av/1_000_000:.2f}M'
        elif av >= 10_000:  s = f'${av/1_000:.1f}k'
        elif av >= 1_000:   s = f'${av/1_000:.2f}k'
        else:               s = f'${av:,.0f}'
    else:
        s = f'${av:,.0f}'
    return f'-{s}' if neg else s


# ── Draw summary header strip ─────────────────────────────────
def _draw_header(ax, stats, accent, label):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(_BG_HEADER)
    ax.axis('off')

    # Scenario pill (left)
    pill = mpatches.FancyBboxPatch(
        (0.01, 0.12), 0.20, 0.76,
        boxstyle='round,pad=0.015',
        facecolor=accent, edgecolor='none',
        transform=ax.transAxes, clip_on=False)
    ax.add_patch(pill)
    ax.text(0.11, 0.50, label,
            transform=ax.transAxes, color=_TXT_HEAD,
            fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Stats bar
    items  = list(stats.items())
    n      = len(items)
    x0, x1 = 0.235, 1.0
    step   = (x1 - x0) / n

    for i, (k, v) in enumerate(items):
        cx = x0 + step * i + step * 0.5
        # Label
        ax.text(cx, 0.72, k,
                transform=ax.transAxes, color=_TXT_COL,
                fontsize=7.5, ha='center', va='center')
        # Value — colour by type
        if isinstance(v, str):
            if v.startswith('-'):    vc = _TXT_NEG
            elif v.startswith('+') or (len(v) > 1 and v[1:].replace(',','').replace('.','').replace('%','').replace('$','').replace('k','').replace('M','').isdigit()):
                vc = _TXT_POS
            else:
                vc = _TXT_NEUT
        else:
            vc = _TXT_NEUT

        ax.text(cx, 0.28, str(v),
                transform=ax.transAxes, color=vc,
                fontsize=10.5, fontweight='bold', ha='center', va='center')

    # Subtle divider line
    ax.axhline(0.0, color=_BORDER, linewidth=0.5)


# ── Draw one year table ───────────────────────────────────────
def _draw_year(ax, year_data, pct_key, usd_key, bal_key,
               accent, accent_dark, account_size):
    ax.set_xlim(0, 1)
    ax.axis('off')
    ax.set_facecolor(_BG_FIG)

    months = year_data['months']
    n_data = len(months) + 1  # rows: months + total

    # Row layout (normalised 0..1 from top)
    H_YR   = 0.068   # year header
    H_COL  = 0.055   # column labels
    H_DATA = (1.0 - H_YR - H_COL) / n_data

    # Column x-positions and widths: Month | % | $ gain | Balance
    CX = [0.00, 0.22, 0.44, 0.68]  # left edges
    CW = [0.22, 0.22, 0.24, 0.32]  # widths

    def rect(x, y, w, h, fc, ec=_BORDER, lw=0.3):
        p = mpatches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle='square,pad=0',
            facecolor=fc, edgecolor=ec, linewidth=lw,
            transform=ax.transAxes, clip_on=False)
        ax.add_patch(p)

    def txt(x, y, s, colour, fs=8.5, bold=False, ha='center'):
        ax.text(x, y, s,
                transform=ax.transAxes, color=colour,
                fontsize=fs, fontweight='bold' if bold else 'normal',
                ha=ha, va='center', clip_on=False)

    # ── Year header ────────────────────────────────────────────
    y = 1.0 - H_YR
    rect(0, y, 1.0, H_YR, accent, ec=accent, lw=0)
    txt(0.5, y + H_YR * 0.5, str(year_data['year']),
        _TXT_HEAD, fs=9.5, bold=True)

    # ── Column labels ──────────────────────────────────────────
    y -= H_COL
    rect(0, y, 1.0, H_COL, _BG_COL_HDR, ec=_BORDER, lw=0.3)
    for ci, (label, cx, cw) in enumerate(zip(
            ['Month', 'Return %', 'Gain / Loss', 'Balance'],
            CX, CW)):
        txt(cx + cw * 0.5, y + H_COL * 0.5, label,
            _TXT_COL, fs=7.5, bold=True)

    # ── Data rows ──────────────────────────────────────────────
    y_cursor = y
    for ri, md in enumerate(months):
        y_cursor -= H_DATA
        bg = _BG_ROW_A if ri % 2 == 0 else _BG_ROW_B
        rect(0, y_cursor, 1.0, H_DATA, bg, ec=_BORDER, lw=0.2)

        pv = md[pct_key]
        uv = md[usd_key]
        bv = md[bal_key]
        pc = _val_colour(pv)
        uc = _val_colour(uv)
        cy = y_cursor + H_DATA * 0.5

        txt(CX[0] + CW[0]*0.5, cy, md['name'],     _TXT_MONTH, fs=8.5)
        txt(CX[1] + CW[1]*0.5, cy, _fmt_pct(pv),   pc,         fs=8.5, bold=True)
        txt(CX[2] + CW[2]*0.5, cy, _fmt_money(uv), uc,         fs=8.5)
        txt(CX[3] + CW[3]*0.5, cy, _fmt_money(bv), _TXT_NEUT,  fs=8.5)

    # ── Total row ──────────────────────────────────────────────
    y_cursor -= H_DATA
    rect(0, y_cursor, 1.0, H_DATA, accent_dark, ec=accent, lw=0.4)

    tv = year_data['total'][pct_key]
    tu = year_data['total'][usd_key]
    tb = year_data['total'][bal_key]

    # Cumulative return from initial balance
    cum_pct = (tb / account_size - 1.0) * 100.0
    cy = y_cursor + H_DATA * 0.5

    txt(CX[0] + CW[0]*0.5, cy, 'Year total',  _TXT_HEAD,      fs=8.0, bold=True)
    txt(CX[1] + CW[1]*0.5, cy, _fmt_pct(tv),  _val_colour(tv),fs=8.5, bold=True)
    txt(CX[2] + CW[2]*0.5, cy, _fmt_money(tu),_val_colour(tu),fs=8.5, bold=True)
    txt(CX[3] + CW[3]*0.5, cy, _fmt_money(tb),_TXT_NEUT,      fs=8.0, bold=True)

    # Cumulative annotation above balance
    txt(CX[3] + CW[3]*0.5, cy + H_DATA * 0.38,
        f'({_fmt_pct(cum_pct)} total)',
        _TXT_COL, fs=6.5)


# ── Main public entry point ───────────────────────────────────
def plot_monthly_breakdown(monthly_table, account_size,
                           extra_stats=None, block=False):
    """
    One figure per scenario (P95 / P50 / P5).
    All years inside that figure. 3 windows total.
    """
    if extra_stats is None:
        extra_stats = {'p95': {}, 'p50': {}, 'p5': {}}

    import matplotlib.patches as mpatches_local
    globals()['mpatches'] = mpatches_local

    n_years      = len(monthly_table)
    COLS         = 3
    n_table_rows = int(np.ceil(n_years / COLS))
    months_tall  = max(len(yd['months']) for yd in monthly_table)

    # Height calc: summary strip + year tables
    H_SUMMARY = 0.85
    H_TABLE   = (months_tall + 2.5) * 0.37   # rows × approx height

    fig_w = min(COLS, n_years) * 5.2
    fig_h = H_SUMMARY + n_table_rows * H_TABLE

    for label, pct_key, usd_key, bal_key, accent, accent_dark, stat_key in _S_META:

        fig = plt.figure(figsize=(fig_w, fig_h), facecolor=_BG_FIG)

        row_h = [H_SUMMARY] + [H_TABLE] * n_table_rows
        gs = gridspec.GridSpec(
            1 + n_table_rows, COLS,
            figure=fig,
            height_ratios=row_h,
            hspace=0.025, wspace=0.018,
            left=0.005, right=0.995,
            top=0.995, bottom=0.005,
        )

        # Summary header
        ax_hdr = fig.add_subplot(gs[0, :])
        _draw_header(ax_hdr, extra_stats.get(stat_key, {}), accent, label)

        # Year tables
        for yi, yd in enumerate(monthly_table):
            row = 1 + yi // COLS
            col = yi % COLS
            ax  = fig.add_subplot(gs[row, col])
            ax.set_facecolor(_BG_FIG)
            _draw_year(ax, yd, pct_key, usd_key, bal_key,
                       accent, accent_dark, float(account_size))

        # Empty cells in last row
        last_row_used = n_years % COLS
        if last_row_used > 0:
            for ec in range(last_row_used, COLS):
                ax_e = fig.add_subplot(gs[n_table_rows, ec])
                ax_e.set_facecolor(_BG_FIG)
                ax_e.axis('off')

        plt.show(block=block)

    return True
