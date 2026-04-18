import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
from modules.components import *

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Loans & Returns")

tab1, tab2, tab3 = st.tabs([
    "Request Logs",
    "Artifact Conditions",
    "Upcoming Returns",
])

# ---- Tab 1: Request Logs (3.5) -----------------------------------------------
with tab1:
    st.subheader("Artifact Request Logs")
    try:
        res = requests.get(f"{API_BASE}/requests/future-returns")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "requestID": "Request ID",
                    "exhibitID": "Exhibit ID",
                    "loaningDonorID": "Donor ID",
                    "requestingEmployeeID": "Requested By",
                    "loanDateStart": "Loan Start",
                    "loanDateEnd": "Loan End",
                    "status": "Status",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No request logs found.")
        else:
            st.error(f"Error fetching request logs (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")

    st.subheader("Artifacts Per Request")
    selected_id = artifact_request_dropdown(key="main_req_picker")
    if selected_id:
        # 2. Add a trigger button
        if st.button(f"Load Artworks for Request #{selected_id}", type="primary"):
            
            try:
                res = requests.get(f"{API_BASE}/requests/{selected_id}/artifacts")
                requested_art = res.json() if res.status_code == 200 else []
            except:
                requested_art = []
            
            artists_res = requests.get(f"{API_BASE}/artists/")
            artists = artists_res.json() if artists_res.status_code == 200 else []
            
            if requested_art:
                st.divider()
                display_artifact_cards(requested_art)
            else:
                st.warning("No artifacts found for this request.")
# ---- Tab 2: Artifact Conditions & Loans (3.4) --------------------------------
with tab2:
    st.subheader("Artifact Condition & Loan Status")
    try:
        res = requests.get(f"{API_BASE}/artifacts")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                display_cols = {
                    "name": "Artifact",
                    "artifactCondition": "Condition",
                    "displayedInExhibitID": "Exhibit ID",
                }
                cols_present = {k: v for k, v in display_cols.items() if k in df.columns}
                df = df[list(cols_present.keys())].rename(columns=cols_present)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No artifacts found.")
        else:
            st.error(f"Error fetching artifacts (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")

# ---- Tab 3: Upcoming Returns (3.6) -------------------------------------------
with tab3:
    st.subheader("Upcoming Artifact Returns")

    use_date_filter = st.checkbox("Filter by return date")
    url = f"{API_BASE}/requests/future-returns"

    if use_date_filter:
        before_date = st.date_input("Show returns due before")
        if before_date:
            if st.button(f"Load Returns", type="primary"):
                url = f"{API_BASE}/requests/before/'{before_date}'"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "requestID": "Request ID",
                    "loaningDonorID": "Donor ID",
                    "loanDateStart": "Loan Start",
                    "loanDateEnd": "Return Date",
                    "status": "Status",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming returns found.")
        else:
            st.error(f"Error fetching returns (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")
                    
