import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Galleries")
st.subheader("Browse and Search Galleries")

with st.expander("Filters", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        filter_name = st.text_input("Gallery Name")
        filter_wing = st.text_input("Wing")
    with col2:
        filter_branch = st.number_input("Branch ID (0 = any)", min_value=0, value=0, step=1)
        filter_capacity = st.number_input("Min Capacity (0 = any)", min_value=0, value=0, step=1)

try:
    params = {}
    if filter_name:
        params["name"] = filter_name
    if filter_wing:
        params["wing"] = filter_wing
    if filter_branch > 0:
        params["branchID"] = filter_branch
    if filter_capacity > 0:
        params["artworkCapacity"] = filter_capacity

    res = requests.get(f"{API_BASE}/galleries/", params=params)
    if res.status_code == 200:
        data = res.json()
        if data:
            st.write(f"**{len(data)} gallery(ies) found**")
            for gallery in data:
                with st.expander(f"{gallery.get('name', 'Unnamed')} — {gallery.get('wing', 'N/A')}"):
                    st.write(f"*Gallery ID:* {gallery.get('galleryID', 'N/A')}")
                    st.write(f"*Wing:* {gallery.get('wing', 'N/A')}")
                    st.write(f"*Capacity:* {gallery.get('artworkCapacity', 'N/A')} artworks")
                    st.write(f"*Branch ID:* {gallery.get('branchID', 'N/A')}")
        else:
            st.info("No galleries found matching your criteria.")
    else:
        st.error(f"Error fetching galleries (HTTP {res.status_code})")
except requests.exceptions.ConnectionError:
    st.warning("Unable to connect to the API.")