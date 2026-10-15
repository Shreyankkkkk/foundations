"""Analytics screens: Overview, Heat Strip, Benchmark, AMD and Evolus."""
import pandas as pd, plotly.graph_objects as go, streamlit as st
from theme import INK, esc, title, big

TYPES = {"skipped_step": "Skipped step", "reordered_steps": "Reordered steps",
         "workaround_substitution": "Workaround or substitution",
         "sop_outdated_or_impractical": "SOP outdated or impractical", "sop_unclear": "SOP unclear"}

def _frame(d):
    f, s = pd.DataFrame(d["flags"]), pd.DataFrame(d["sop"])
    if f.empty or s.empty:
        return f, s
    s["label"] = s.sop_id.str.replace("SOP-", "") + " " + s.step_id.astype(str) + ". " + s.title
    f["date"] = pd.to_datetime(f["date"])
    f["week"] = f["date"].dt.isocalendar().week.astype(int)  # week numbers come from the date
    return f.merge(s[["sop_id", "step_id", "text", "label"]], on=["sop_id", "step_id"], how="left"), s

def _trend(f, label):
    wk, g = f.week.max(), f[f.label == label]
    now = int((g.week >= wk - 1).sum())  # last 2 weeks vs the 2 before
    prev = int(((g.week >= wk - 3) & (g.week <= wk - 2)).sum())
    if now > prev: return f"&#9650; rising ({prev} to {now})", "up"
    if now < prev: return f"&#9660; easing ({prev} to {now})", ""
    return "&#9644; steady", ""

def overview(d):
    f, _ = _frame(d); b = d["benchmark"]
    st.markdown(title("Which steps drift most?", "Routine shift notes read against the written procedures. Every flag carries a quote that code checked word for word."), unsafe_allow_html=True)
    if f.empty:
        st.info("No flags yet. Run the pipeline, or switch Demo mode on in the sidebar."); return
    nums = [(len(d["notes"]), "notes read"), (len(f), "flags raised"),
            (round(len(f) * b["quote_verified_rate"]), "quotes verified"), (int((f.status == "approved").sum()), "approved by a person")]
    for col, (v, l) in zip(st.columns(4), nums):
        col.markdown(big(v, l), unsafe_allow_html=True)
    st.markdown("<h3 class='sec'>Top 3 drifting steps</h3>", unsafe_allow_html=True)
    top = f.groupby("label").size().sort_values(ascending=False).head(3)
    rows = ""
    for i, (lab, n) in enumerate(top.items(), 1):
        t, c = _trend(f, lab)
        rows += (f"<div class='row rise' style='animation-delay:{i * .12:.2f}s'><div class='rk'><span class='plate'>{i}</span></div><div class='nm'>{esc(lab)}<div class='bar'>"
                 f"<i style='animation-delay:{.35 + i * .12:.2f}s;width:{n / top.iloc[0] * 100:.0f}%'></i></div></div><div class='ct'>{n}</div><div class='tr {c}'>{t}</div></div>")
    st.markdown(rows + "<div class='row' style='padding:0'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub' style='margin-top:1.5rem'>Matching and judging run on {esc(b['gpu'])} at {b['notes_per_minute']:.0f} notes per minute. "
                f"Open Heat Strip to see when each step started drifting.</div>", unsafe_allow_html=True)

def heat_strip(d):
    f, s = _frame(d)
    st.markdown(title("Where does practice drift, and is it growing?", "Darker tiles mean more flags. Click a tile, or pick a step below, to read the notes behind it."), unsafe_allow_html=True)
    if f.empty:
        st.info("No flags yet. Run the pipeline, or switch Demo mode on in the sidebar."); return
    with st.sidebar:
        st.markdown("**Filters**")
        sops = st.multiselect("SOP", sorted(f.sop_id.unique()), default=sorted(f.sop_id.unique()))
        shifts = st.multiselect("Shift", sorted(f["shift"].unique()), default=sorted(f["shift"].unique()))
        types = st.multiselect("Drift type", list(TYPES), default=list(TYPES), format_func=TYPES.get)
    g = f[f.sop_id.isin(sops) & f["shift"].isin(shifts) & f.drift_type.isin(types)]
    if g.empty:
        st.info("No flags match these filters. Widen them in the sidebar."); return
    weeks = list(range(int(f.week.min()), int(f.week.max()) + 1))
    labels = list(s[s.sop_id.isin(sops)].label)
    z = g.pivot_table(index="label", columns="week", values="flag_id", aggfunc="count", fill_value=0).reindex(index=labels, columns=weeks, fill_value=0)
    fig = go.Figure(go.Heatmap(z=z.values, x=[f"Week {w}" for w in weeks], y=labels, xgap=4, ygap=4, showscale=False,
                               colorscale=[[0, "#DCE3E6"], [1, INK]], text=z.astype(str).where(z > 0, "").values, texttemplate="%{text}",
                               hovertemplate="%{y}<br>%{x}: %{z} flags<extra></extra>"))
    fig.update_layout(height=70 + 44 * len(labels), margin=dict(l=0, r=0, t=30, b=0), dragmode=False,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Archivo, system-ui, sans-serif", size=15, color=INK),
                      xaxis=dict(side="top", fixedrange=True, showgrid=False),
                      yaxis=dict(autorange="reversed", fixedrange=True, showgrid=False, automargin=True))
    ev = st.plotly_chart(fig, key="heat", on_select="rerun", selection_mode="points", config={"displayModeBar": False})
    pts = ev.selection.points if ev and ev.selection else []
    clicked = pts[0].get("y") if pts else None
    ranked = list(g.groupby("label").size().sort_values(ascending=False).index)
    default = clicked if clicked in labels else ranked[0]
    pick = st.selectbox("Step", labels, index=labels.index(default))
    sel = g[g.label == pick].sort_values("date", ascending=False)
    t, c = _trend(g, pick)
    st.markdown(f"<h3 class='sec' style='margin-top:1.6rem'>{esc(pick)}</h3><span class='tr {c}'>{t}</span>"
                f"<div class='stepbox'>{esc(str(s.loc[s.label == pick, 'text'].iloc[0]))}</div>", unsafe_allow_html=True)
    if sel.empty:
        st.info("No flags for this step with the current filters."); return
    for k, r in enumerate(sel.itertuples()):
        st.markdown(f"<div class='flag rise' style='animation-delay:{min(k, 8) * .07:.2f}s'><span class='chip'>{TYPES.get(r.drift_type, r.drift_type)}</span><span class='chip'>{r.status}</span>"
                    f"<blockquote>{esc(r.quote)}</blockquote><div class='meta'>{r.date:%d %b}, {esc(r.shift)} shift. "
                    f"Confidence {r.confidence:.0%}.</div></div>", unsafe_allow_html=True)

def benchmark(d):
    b, (f, _) = d["benchmark"], _frame(d)
    st.markdown(title("How accurate is it, and where is it wrong?", "Scored against drifts we planted on purpose, with an answer key. False alarms are listed in full below."), unsafe_allow_html=True)
    vals = [(f"{b['precision']:.0%}", "precision"), (f"{b['recall']:.0%}", "recall"),
            (f"{b['quote_verified_rate']:.0%}", "quote-verified rate"), (f"{b['notes_per_minute']:.0f}", "notes per minute")]
    for col, (v, l) in zip(st.columns(4), vals):
        col.markdown(big(v, l), unsafe_allow_html=True)
    st.markdown("<h3 class='sec'>Results</h3>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Measure": [l for _, l in vals],
        "Value": [v for v, _ in vals],
        "What it means": ["Of the flags we raised, how many were real drift.", "Of the real drifts, how many we found.",
                          "Share of quotes that appear word for word in the note.", "How many notes the AI reads per minute."]}),
        hide_index=True, width="stretch")
    st.markdown("<h3 class='sec'>Where our AI is wrong</h3>", unsafe_allow_html=True)
    if f.empty or not b.get("false_alarms"):
        st.info("No false alarms recorded in this run."); return
    w = f[f.flag_id.isin(b["false_alarms"])]
    st.dataframe(pd.DataFrame({"Step": w.label, "Drift type": w.drift_type.map(TYPES), "Quote": w.quote, "Confidence": w.confidence.map("{:.0%}".format)}),
                 hide_index=True, width="stretch")
    st.caption("A flag asks a person to look. It is never a verdict.")

def amd(d):
    a, b = d["amd"], d["benchmark"]
    st.markdown(title("What runs on AMD, and how fast?", "The AMD GPU powers matching and judging in this product. Figures come from the last run."), unsafe_allow_html=True)
    for col, (v, l) in zip(st.columns(4), [(a["endpoint_status"].capitalize(), "endpoint status"), (f"{b['notes_per_minute']:.0f}", "notes per minute"),
                                           (f"${a['cost_per_1000_notes']:.2f}", "cost per 1,000 notes"), (f"{a['evolus_api_calls']:,}", "Evolus API calls")]):
        col.markdown(big(v, l), unsafe_allow_html=True)
    st.markdown("<h3 class='sec'>Two models, one GPU</h3>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Job": ["Match notes to steps", "Judge drift"], "Model": [b["matcher_model"], b["judge_model"]], "GPU": [b["gpu"]] * 2}),
                 hide_index=True, width="stretch")
    st.markdown("<h3 class='sec'>Evolus building blocks used</h3>" + "".join(f"<span class='chip'>{esc(x)}</span>" for x in a["evolus_blocks"]), unsafe_allow_html=True)
