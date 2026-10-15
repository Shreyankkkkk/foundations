"""Loads data. Live = the back end's endpoint (set DRIFT_API_URL as an environment variable).
Demo = saved JSON files in data/. The address is never shown on screen."""
import json, os, urllib.request
import streamlit as st
from config import DATA_DIR as D, KEYS, API_URL_ENV, API_TIMEOUT_S, CACHE_TTL_S

def _read(k):
    return json.loads((D / f"{k}.json").read_text(encoding="utf-8"))

def _live(k):
    base = os.getenv(API_URL_ENV)
    if not base:
        raise RuntimeError("no endpoint set")
    with urllib.request.urlopen(f"{base.rstrip('/')}/{k}", timeout=API_TIMEOUT_S) as r:
        return json.load(r)

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
    dec = D / "decisions.json"  # assumed shape: {"flag_id": "approved" | "rejected"}
    if dec.exists():
        m = json.loads(dec.read_text(encoding="utf-8"))
        for f in out["flags"]:
            f["status"] = m.get(str(f["flag_id"]), f["status"])
    return out, mode
