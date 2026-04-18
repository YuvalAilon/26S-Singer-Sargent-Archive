import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Museum Statistics")

tab1, tab2 = st.tabs([
    "Styles by Branch",
    "Exhibit Activity",
])

# ---- Tab 1: Styles by Branch (4.2) -------------------------------------------
with tab1:
    st.subheader("Artifact Counts by Style, per Branch")
    try:
        res = requests.get(f"{API_BASE}/artifacts/style-counts")
        if res.status_code == 200:
            data = res.json()
            if not data:
                st.info("No style data available.")
            else:
                df = pd.DataFrame(data).rename(columns={
                    "branchName": "Branch",
                    "style": "Style",
                    "artifactCount": "Artifact Count",
                })

                branches = ["All"] + sorted(df["Branch"].dropna().unique().tolist()) \
                    if "Branch" in df.columns else ["All"]
                chosen = st.selectbox("Filter by Branch", branches)
                view_df = df if chosen == "All" else df[df["Branch"] == chosen]
                st.dataframe(view_df, use_container_width=True, hide_index=True)
        else:
            st.error(f"Error fetching style counts (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")


# ---- Tab 2: Exhibit Activity (4.7) -------------------------------------------
with tab2:
    st.subheader("Exhibit Activity by Branch")
    try:
        res = requests.get(f"{API_BASE}/exhibits/branch-stats")
        if res.status_code == 200:
            data = res.json()
            if not data:
                st.info("No exhibit activity data available.")
            else:
                df = pd.DataFrame(data).rename(columns={
                    "branchName": "Branch",
                    "totalExhibits": "Total Exhibits",
                    "earliestExhibit": "Earliest Exhibit",
                    "mostRecentExhibit": "Most Recent Exhibit",
                    "exhibitsPerMonth": "Exhibits per Month",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error(f"Error fetching exhibit stats (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")
