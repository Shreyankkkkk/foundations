import streamlit as st
from theme import CSS, banner
from data_loader import get_data
from views import analytics

st.set_page_config(page_title="Procedure Drift Finder", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

PAGES = {"Overview": analytics.overview, "Heat Strip": analytics.heat_strip, "Review Queue": None,
         "Evidence Viewer": None, "Benchmark": analytics.benchmark, "AMD and Evolus": analytics.amd}
try:  # views/review.py exposes a PAGES dict {"Review Queue": fn, ...}
    from views import review
    PAGES.update(review.PAGES)
except ImportError:
    pass

with st.sidebar:
    st.markdown("### Procedure Drift Finder")
    page = st.radio("Page", list(PAGES), label_visibility="collapsed", key="page")
    demo = st.toggle("Demo mode", value=True, help="Loads saved results from the data folder.")
    st.caption("All data in this app is synthetic.")

try:
    d, mode = get_data(demo)
    if not demo and mode == "demo":
        st.warning("The live pipeline did not answer, so saved results are shown instead.")
    st.markdown(banner(mode), unsafe_allow_html=True)
    if PAGES[page] is None:
        st.info("This screen is built on the other branch and appears here after the merge.")
    else:
        PAGES[page](d)
except Exception as e:
    st.error(f"This page could not load ({type(e).__name__}). Check that the files in data/ match the agreed format, or switch Demo mode on.")
