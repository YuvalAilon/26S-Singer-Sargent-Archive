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

st.title("Browse the Collection")

tab1, tab2, tab3 = st.tabs([
    "All Artifacts",
    "Search by Name",
    "Advanced Filter",
])

BASE_RENAME = {
    "name": "Artwork",
    "createdYear": "Year",
    "firstName": "Artist First",
    "middleName": "Artist Middle",
    "lastName": "Artist Last",
    "style": "Style",
    "medium": "Medium",
    "artifactCondition": "Condition",
    "archivistFirstName": "Archivist",
    "displayedInExhibitID": "Exhibit ID",
}


def render_table(data):
    if not data:
        st.info("No artifacts matched.")
        return
    display_artifact_cards(data)
    


# ---- Tab 1: All Artifacts (4.1) ----------------------------------------------
with tab1:
    st.subheader("The Museum's Complete Collection")
    try:
        res = requests.get(f"{API_BASE}/artifacts/filter")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                if "createdYear" in df.columns:
                    df = df.sort_values("createdYear", na_position="last")
                render_table(
                    df.to_dict(orient="records"),
                )
            else:
                st.info("No artifacts found.")
        else:
            st.error(f"Error fetching artifacts (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")


# ---- Tab 2: Search by Name (4.3) ---------------------------------------------
with tab2:
    st.subheader("Find an Artwork by Name")
    name_query = st.text_input("Artwork name contains", value="", key="name_search")
    if st.button("Search", key="name_search_btn"):
        try:
            res = requests.get(
                f"{API_BASE}/artifacts/filter", params={"name": name_query}
            )
            if res.status_code == 200:
                render_table(
                    res.json())
            else:
                st.error(f"Error searching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")


# ---- Tab 3: Advanced Filter (4.5) --------------------------------------------
with tab3:
    st.subheader("Filter Artifacts")
    with st.form("artifact_filter_form"):
        f_name = st.text_input("Name contains")
        f_style = st.text_input("Style contains")
        f_artist = st.text_input("Artist name contains")
        year_start, year_end = st.slider(
            "Created year range",
            min_value=1000,
            max_value=2100,
            value=(1700, 1900),
        )
        submitted = st.form_submit_button("Apply Filters")

    if submitted:
        params = {
            "dateAfter": year_start,
            "dateBefore": year_end,
        }
        if f_name:
            params["name"] = f_name
        if f_style:
            params["style"] = f_style
        if f_artist:
            params["artistName"] = f_artist
        try:
            res = requests.get(f"{API_BASE}/artifacts/filter", params=params)
            if res.status_code == 200:
                render_table(
                    res.json(),
                )
            else:
                st.error(f"Error fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")
