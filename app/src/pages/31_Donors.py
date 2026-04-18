import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Donors & Donations")

tab1, tab2, tab3 = st.tabs([
    "Donation History",
    "Donor Directory",
    "Top Donors",
])

# ---- Tab 1: Donation History (3.1, 3.2.2) ------------------------------------
with tab1:
    st.subheader("Donations")

    try:
        res = requests.get(f"{API_BASE}/donors/donations")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "contactFirstName": "First Name",
                    "contactLastName": "Last Name",
                    "amount": "Amount ($)",
                    "reason": "Reason",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No donations on record.")
        else:
            st.error(f"Error fetching donations (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")


# ---- Tab 2: Donor Directory (3.2.1) ------------------------------------------
with tab2:
    st.subheader("Donors Who Have Contributed")
    try:
        res = requests.get(f"{API_BASE}/donors")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                display_cols = {
                    "contactFirstName": "First Name",
                    "contactLastName": "Last Name",
                    "email": "Email",
                    "organizationName": "Organization",
                }
                cols_present = {k: v for k, v in display_cols.items() if k in df.columns}
                df = df[list(cols_present.keys())].rename(columns=cols_present)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No donors found.")
        else:
            st.error(f"Error fetching donors (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")


# ---- Tab 3: Top Donors (3.3.1, 3.3.2) ----------------------------------------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Monetary Donors")
        count_m = st.slider(
            "Number of donors", min_value=5, max_value=100, value=50, key="cnt_m"
        )
        try:
            res = requests.get(
                f"{API_BASE}/donors/top-monetary", params={"count": count_m}
            )
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "contactFirstName": "First Name",
                        "contactLastName": "Last Name",
                        "email": "Email",
                        "total_donations": "Total Donated ($)",
                    })
                    df.index = range(1, len(df) + 1)
                    df.index.name = "Rank"
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No monetary donors found.")
            else:
                st.error(f"Error (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

    with col2:
        st.subheader("Top Artifact Lenders")
        count_a = st.slider(
            "Number of lenders", min_value=5, max_value=100, value=25, key="cnt_a"
        )
        try:
            res = requests.get(
                f"{API_BASE}/donors/top-artifact", params={"count": count_a}
            )
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "contactFirstName": "First Name",
                        "contactLastName": "Last Name",
                        "email": "Email",
                        "pieces_donated": "Pieces Lent",
                    })
                    df.index = range(1, len(df) + 1)
                    df.index.name = "Rank"
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No artifact lenders found.")
            else:
                st.error(f"Error (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")
