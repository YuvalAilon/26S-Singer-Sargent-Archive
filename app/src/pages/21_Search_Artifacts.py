import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Search & Filter Artifacts")

tab1, tab2 = st.tabs(["Search Collection", "Artifact Locations"])

# ------ Tab 1: Search / Filter ------------------------------------------
with tab1:
    st.subheader("Filter by Artist, Style, Medium, and More")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_name = st.text_input("Artifact Name")
        filter_artist = st.text_input("Artist Name")
    with col2:
        filter_style = st.text_input("Style")
        filter_condition = st.selectbox("Condition",
                                         ["Any", "pristine", "good", "fair", "poor", "requires restoration"])
    with col3:
        filter_date_after = st.number_input("Year After", min_value=0, max_value=2026, value=0, step=1)
        filter_date_before = st.number_input("Year Before", min_value=0, max_value=2026, value=2026, step=1)

    if st.button("Search", type="primary"):
        try:
            params = {}
            if filter_name:
                params["name"] = filter_name
            if filter_artist:
                params["artistName"] = filter_artist
            if filter_style:
                params["style"] = filter_style
            if filter_condition != "Any":
                params["condition"] = filter_condition
            if filter_date_after > 0:
                params["dateAfter"] = filter_date_after
            if filter_date_before < 2026:
                params["dateBefore"] = filter_date_before

            res = requests.get(f"{API_BASE}/artifacts/filter", params=params)
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "artifactID": "ID",
                        "name": "Artifact",
                        "style": "Style",
                        "medium": "Medium",
                        "createdYear": "Year",
                        "artifactCondition": "Condition",
                        "firstName": "Artist First",
                        "lastName": "Artist Last",
                        "displayedInExhibitID": "Exhibit ID",
                    })
                    display_cols = [c for c in ["ID", "Artifact", "Artist First", "Artist Last",
                                                 "Style", "Medium", "Year", "Condition", "Exhibit ID"]
                                    if c in df.columns]
                    st.write(f"**{len(data)} artifact(s) found**")
                    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
                else:
                    st.info("No artifacts found matching your criteria.")
            else:
                st.error(f"Error fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

# ------ Tab 2: Artifact Locations ----------------------------------------
with tab2:
    st.subheader("Current Artifact Locations")
    try:
        res = requests.get(f"{API_BASE}/artifacts")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "artifactID": "ID",
                    "name": "Artifact",
                    "displayedInExhibitID": "Exhibit ID",
                    "artifactCondition": "Condition",
                })
                display_cols = [c for c in ["ID", "Artifact", "Exhibit ID", "Condition"] if c in df.columns]
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
            else:
                st.info("No artifacts found.")
        else:
            st.error(f"Error fetching artifacts (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")