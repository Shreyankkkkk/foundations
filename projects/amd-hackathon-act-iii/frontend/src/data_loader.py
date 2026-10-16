"""Loads data. Live = the back end's endpoint (set DRIFT_API_URL as an environment variable).
Demo = saved JSON files in data/. The address is never shown on screen."""
import json, os, urllib.request
import streamlit as st
from config import DATA_DIR as D, KEYS, API_URL_ENV, API_TIMEOUT_S, CACHE_TTL_S

DECISIONS = D / "decisions.json"  # {"flag_id": "approved" | "rejected" | "pending"}
# amd.json only exists after the first real run is published, so the app starts without it.
EMPTY_AMD = {"endpoint_status": None, "cost_per_1000_notes": None, "evolus_api_calls": None, "evolus_blocks": []}

class DataError(Exception):
    """A file in data/ is missing or is not valid JSON. The message says which one."""

def _read(k):
    try:
        return json.loads((D / f"{k}.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        if k == "amd":
            return dict(EMPTY_AMD)
        raise DataError(f"data/{k}.json is missing.") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise DataError(f"data/{k}.json is not valid JSON.") from None

def _live(k):
    base = os.getenv(API_URL_ENV)
    if not base:
        raise RuntimeError("no endpoint set")
    with urllib.request.urlopen(f"{base.rstrip('/')}/{k}", timeout=API_TIMEOUT_S) as r:
        return json.load(r)

def read_decisions():
    """Saved approve/reject choices. A damaged file counts as 'no decisions yet' instead of breaking every page."""
    try:
        m = json.loads(DECISIONS.read_text(encoding="utf-8"))
        return m if isinstance(m, dict) else {}
    except (OSError, ValueError):
        return {}

def save_decision(flag_id, status):
    m = read_decisions()
    m[str(flag_id)] = status
    temp = DECISIONS.with_suffix(".tmp")  # write a temp file, then swap it in, so a crash never leaves half a file
    temp.write_text(json.dumps(m, indent=1), encoding="utf-8")
    temp.replace(DECISIONS)
    get_data.clear()

@st.cache_data(ttl=CACHE_TTL_S, show_spinner="Loading results...")
def get_data(want_demo):
    out, mode = {}, "demo"
    if not want_demo:
        try:
            out = {k: _live(k) for k in KEYS}
            mode = "live"
        except Exception:
            out = {}
    if not out:
        out = {k: _read(k) for k in KEYS}
    m = read_decisions()
    for f in out["flags"]:
        f["status"] = m.get(str(f["flag_id"]), f["status"])
    return out, mode
