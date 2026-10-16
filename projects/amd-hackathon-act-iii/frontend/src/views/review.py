"""Review screens: Review Queue, Evidence Viewer, SOP-fix box (always labelled DRAFT)."""
import pandas as pd, streamlit as st
from theme import esc, title
from data_loader import save_decision
from views.analytics import TYPES, _frame
from quote import quote_span

def _save(fid, status):
    save_decision(fid, status)

def _goto(fid):
    st.session_state["page"], st.session_state["ev_flag"] = "Evidence Viewer", fid

def _note(r, notes):
    n, q = notes.get(r["note_id"]), r["quote"]
    span = quote_span(n["text"], q) if n else None
    if span is None:
        return esc(n["text"] if n else q), "<span class='chip bad'>&#9888; Quote not found in the note: drop this flag</span>"
    t, (i, j) = n["text"], span
    return f"{esc(t[:i])}<mark class='hl'>{esc(t[i:j])}</mark>{esc(t[j:])}", "<span class='chip ok'>&#10003; Quote found word for word</span>"

def _chips(r):
    low = r["confidence"] < .7
    return (f"<span class='chip'>{esc(TYPES.get(r['drift_type'], r['drift_type']))}</span>"
            f"<span class='chip {'low' if low else ''}'>{'&#9650; Look closely. ' if low else ''}Confidence {r['confidence']:.0%}</span>")

def _fix(r):
    if r["drift_type"] in ("sop_outdated_or_impractical", "sop_unclear") and r["suggested_fix"]:
        return f"<div class='draft rise'><span class='tag'>Draft, needs human approval</span>{esc(r['suggested_fix'])}</div>"
    return ""

def review_queue(d):
    f, _ = _frame(d); notes = {n["note_id"]: n for n in d["notes"]}
    st.markdown(title("Which flags need a person's decision?", "Least certain first. Read the evidence, then approve or reject. Decisions are saved."), unsafe_allow_html=True)
    if f.empty:
        st.info("No flags yet. Run the pipeline, or switch Demo mode on in the sidebar."); return
    c1, c2 = st.columns([1, 1])
    stat = c1.segmented_control("Status", ["pending", "approved", "rejected", "all"], default="pending") or "pending"
    kinds = c2.multiselect("Drift type", list(TYPES), default=list(TYPES), format_func=TYPES.get)
    done = int((f.status != "pending").sum())
    st.progress(done / len(f), text=f"{done} of {len(f)} flags decided")
    g = f[f.drift_type.isin(kinds)]
    g = (g if stat == "all" else g[g.status == stat]).sort_values("confidence")
    if g.empty:
        st.success("Nothing in this view. Change the filters, or enjoy an empty queue."); return
    view = pd.DataFrame({"Step": g.label, "Drift type": g.drift_type.map(TYPES), "Shift": g["shift"], "Date": g.date.dt.strftime("%d %b"),
                         "Confidence": (g.confidence * 100).round().astype(int), "Status": g.status})
    ev = st.dataframe(view, hide_index=True, on_select="rerun", selection_mode="single-row", key=f"rq_{done}_{stat}", height=min(340, 38 * len(view) + 40),
                      column_config={"Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100, format="%d%%")})
    r = g.iloc[ev.selection.rows[0] if ev and ev.selection.rows else 0]
    body, chip = _note(r, notes)
    left, right = st.columns([3, 2], gap="large")
    left.markdown(f"<h3 class='sec' style='margin-top:1.6rem'><span class='plate'>{int(r['step_id'])}</span>{esc(r['label'])}</h3>"
                  f"<div class='stepbox'>{esc(r['text'])}</div><div class='note rise'>{body}</div>{chip}", unsafe_allow_html=True)
    with right:
        st.markdown(f"<h3 class='sec' style='margin-top:1.6rem'>AI proposed</h3><div class='card'>{_chips(r)}<div class='meta'>{esc(r['shift'])} shift, {r['date']:%d %b}. "
                    f"Now: <b>{esc(r['status'])}</b></div></div>", unsafe_allow_html=True)
        a, b = st.columns(2); fid = r["flag_id"]
        a.button("Approve", key=f"ok{fid}", type="primary", width="stretch", on_click=_save, args=(fid, "approved"))
        b.button("Reject", key=f"no{fid}", width="stretch", on_click=_save, args=(fid, "rejected"))
        if r["status"] != "pending":
            st.button("Back to pending", key=f"un{fid}", width="stretch", on_click=_save, args=(fid, "pending"))
        st.button("Open in Evidence Viewer", key=f"ev{fid}", width="stretch", on_click=_goto, args=(fid,))
        st.markdown(_fix(r), unsafe_allow_html=True)

def evidence_viewer(d):
    f, _ = _frame(d); notes = {n["note_id"]: n for n in d["notes"]}
    st.markdown(title("Does the note really contradict the step?", "Left: the written step. Middle: the exact words from the note. Right: the same step on other shifts."), unsafe_allow_html=True)
    if f.empty:
        st.info("No flags yet. Run the pipeline, or switch Demo mode on in the sidebar."); return
    f = f.sort_values("confidence", ascending=False)
    lab = {x.flag_id: f"{x.flag_id}: {x.label} ({x.shift}, {x.date:%d %b})" for x in f.itertuples()}
    if st.session_state.get("ev_flag") not in lab:  # a flag chosen before the data changed no longer exists
        st.session_state.pop("ev_flag", None)
    fid = st.selectbox("Flag", list(lab), format_func=lab.get, key="ev_flag")
    r = f[f.flag_id == fid].iloc[0]
    body, chip = _note(r, notes)
    c1, c2, c3 = st.columns([1, 1.5, 1], gap="large")
    c1.markdown(f"<div class='lbl'>Written step</div><h3 class='sec' style='margin-top:.6rem'><span class='plate'>{int(r['step_id'])}</span></h3>"
                f"<b>{esc(r['label'])}</b><div class='stepbox rise'>{esc(r['text'])}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='lbl'>What the note says</div><div class='note'>{body}</div>{chip}{_chips(r)}"
                f"<div class='meta'>{esc(r['shift'])} shift, {r['date']:%d %b}, status {esc(r['status'])}</div>", unsafe_allow_html=True)
    o = f[(f.sop_id == r["sop_id"]) & (f.step_id == r["step_id"]) & (f["shift"] != r["shift"])].sort_values("date", ascending=False).head(4)
    cards = "".join(f"<div class='card rise' style='animation-delay:{.12 * (k + 1):.2f}s'><div class='meta'>{esc(x.shift)} shift, {x.date:%d %b}</div>{esc(x.quote)}</div>" for k, x in enumerate(o.itertuples()))
    c3.markdown(f"<div class='lbl'>Same step, other shifts</div><div style='height:.8rem'></div>{cards or '<div class=meta>No similar notes from other shifts.</div>'}", unsafe_allow_html=True)
    st.markdown(_fix(r), unsafe_allow_html=True)

PAGES = {"Review Queue": review_queue, "Evidence Viewer": evidence_viewer}
