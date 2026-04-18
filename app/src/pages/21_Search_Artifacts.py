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
st.subheader("Filter by Artist, Style, Medium, and More")

with st.expander("Search Filters", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_name = st.text_input("Artifact Name")
        filter_artist = st.text_input("Artist Name")
    with col2:
        filter_style = st.selectbox("Style",
                                     ["Any", "realism", "Impressionism", "rococo",
                                      "pop art", "renaissance", "Postmodernism"])
        filter_condition = st.selectbox("Condition",
                                         ["Any", "pristine", "good", "fair",
                                          "poor", "requires restoration"])
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
        if filter_style != "Any":
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
                st.write(f"**{len(data)} artifact(s) found**")
                for item in data:
                    st.divider()
                    col_img, col_info = st.columns([1, 2])
                    with col_img:
                        if item.get('imageURL'):
                            st.image(item['imageURL'], use_container_width=True)
                        else:
                            st.write("*No image available*")
                    with col_info:
                        st.write(f"### {item.get('name', 'Untitled')}")
                        st.write(f"*Artist:* {item.get('firstName', '')} {item.get('lastName', 'Unknown')}")
                        st.write(f"*Style:* {item.get('style', 'N/A')}")
                        st.write(f"*Medium:* {item.get('medium', 'N/A')}")
                        st.write(f"*Year:* {item.get('createdYear', 'N/A')}")
                        st.write(f"*Condition:* {item.get('artifactCondition', 'N/A')}")
                        st.write(f"*Exhibit ID:* {item.get('displayedInExhibitID', 'N/A')}")
            else:
                st.info("No artifacts found matching your criteria.")
        else:
            st.error(f"Error fetching artifacts (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")