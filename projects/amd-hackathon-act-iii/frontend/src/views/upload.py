"""Add Documents screen: upload SOPs and notes, fix them in a table, check them, export the backend's two input files."""
import hashlib, json
from datetime import date
import pandas as pd, streamlit as st
import ingest
from config import DATA_DIR
from theme import esc, title

UPLOAD_DIR = DATA_DIR / "uploads"  # ignored by Git on purpose: uploads may be real plant data
KINDS = ["pdf", "docx", "txt", "md", "csv", "json"]

def _plate(n, text):
    return f"<h3 class='sec' style='margin-top:2.6rem'><span class='plate'>{n}</span>{esc(text)}</h3>"

def _safe(f, parse):
    try:
        return parse(f.name, f.getvalue())
    except ImportError:
        st.warning(f"Cannot read {f.name}: a reader library is missing. Run pip install -r requirements.txt.")
    except Exception as e:
        st.warning(f"Could not read {f.name} ({type(e).__name__}: {str(e)[:90]}). Try saving it as .docx, .txt or .csv.")
    return []

def _sig(*parts):
    return hashlib.md5(json.dumps(parts, default=str).encode()).hexdigest()[:8]  # new files = fresh table

def add_documents(d):
    st.markdown(title("Are these documents ready for the pipeline?", "Add SOPs and shift notes as Word, PDF, text, CSV or JSON. We turn them into the backend's two input files and check them before you export."), unsafe_allow_html=True)
    st.markdown("<div class='card rise'><b>Before you upload:</b> keep it about steps and shifts, and remove personal names. "
                "Files are read on this computer and saved only to <code>data/uploads/</code>, which Git ignores.</div>", unsafe_allow_html=True)
    sample = st.toggle("Use the built-in sample data instead of my files", key="up_sample")
    c = st.columns(3)
    defaults = {"date": c[0].date_input("Date for notes that have none", value=date.today()).isoformat(),
                "shift": c[1].selectbox("Shift for notes that have none", ingest.SHIFTS),
                "source": c[2].selectbox("Type for notes that have none", ingest.SOURCES)}

    st.markdown(_plate(1, "Add the SOPs"), unsafe_allow_html=True)
    sop_files = [] if sample else (st.file_uploader("SOP documents. One SOP per file; numbered lines become steps.", type=KINDS, accept_multiple_files=True, key="up_sop") or [])
    steps = d["sop"] if sample else [s for k, f in enumerate(sop_files, 1) for s in _safe(f, lambda n, b, k=k: ingest.parse_sop_file(n, b, f"SOP-{k:02d}"))]
    sdf = pd.DataFrame(steps, columns=ingest.STEP_FIELDS)
    if sdf.empty:
        st.info("No SOP steps yet. Add a file above, switch on the sample data, or type rows into the table.")
    sdf = st.data_editor(sdf, num_rows="dynamic", hide_index=True, width="stretch", key=f"sop_{_sig([f.name for f in sop_files], sample)}",
                         column_config={"step_id": st.column_config.NumberColumn("step_id", step=1, format="%d"), "text": st.column_config.TextColumn("text", width="large")})
    steps = ingest.clean_steps(sdf.to_dict("records"))

    st.markdown(_plate(2, "Add the shift notes"), unsafe_allow_html=True)
    note_files = [] if sample else (st.file_uploader("Notes. CSV or JSON with a text column, or a document with one note per paragraph.", type=KINDS, accept_multiple_files=True, key="up_notes") or [])
    raw = d["notes"] if sample else [n for f in note_files for n in _safe(f, ingest.parse_notes_file)]
    notes = raw if sample else ingest.finish_notes(raw, defaults)
    ndf = pd.DataFrame(notes, columns=ingest.NOTE_FIELDS)
    if ndf.empty:
        st.info("No notes yet. Add a file above, switch on the sample data, or type rows into the table.")
    ndf = st.data_editor(ndf, num_rows="dynamic", hide_index=True, width="stretch", key=f"notes_{_sig([f.name for f in note_files], sample, defaults)}",
                         column_config={"source": st.column_config.SelectboxColumn("source", options=ingest.SOURCES), "text": st.column_config.TextColumn("text", width="large")})
    notes = ingest.clean_notes(ndf.to_dict("records"))

    st.markdown(_plate(3, "Check and export"), unsafe_allow_html=True)
    errors, warnings = ingest.validate(steps, notes)
    if errors:
        st.error("Fix these before exporting:\n\n" + "\n".join(f"- {e}" for e in errors[:8]) + (f"\n\n...and {len(errors) - 8} more." if len(errors) > 8 else ""))
    else:
        st.markdown(f"<span class='chip ok'>&#10003; Ready: {len(steps)} steps in {len({s['sop_id'] for s in steps})} SOPs, {len(notes)} notes</span>", unsafe_allow_html=True)
    if warnings:
        st.warning("\n".join(f"- {w}" for w in warnings[:5]))
    a, b, s = st.columns(3)
    a.download_button("Download sop.json", ingest.to_json(steps), "sop.json", "application/json", disabled=bool(errors), width="stretch")
    b.download_button("Download notes.json", ingest.to_json(notes), "notes.json", "application/json", disabled=bool(errors), width="stretch")
    if s.button("Save a copy in this app", disabled=bool(errors), width="stretch"):
        UPLOAD_DIR.mkdir(exist_ok=True)
        (UPLOAD_DIR / "sop.json").write_text(ingest.to_json(steps), encoding="utf-8")
        (UPLOAD_DIR / "notes.json").write_text(ingest.to_json(notes), encoding="utf-8")
        st.success("Saved to data/uploads/sop.json and notes.json.")
    st.markdown("<h3 class='sec'>Hand them to the backend</h3>", unsafe_allow_html=True)
    st.code("copy data\\uploads\\sop.json ..\\backend\\data\\sop.json\ncopy data\\uploads\\notes.json ..\\backend\\data\\notes.json\n"
            "cd ..\\backend\npython -m src.pipeline --fake\ncd ..\\frontend\npython scripts\\sync_backend_data.py --source fake", language="powershell")
    st.caption("This replaces the backend's sample files (undo with git checkout on backend/data). Benchmark scores only make sense for the sample notes, because the answer key belongs to them.")

PAGES = {"Add Documents": add_documents}
