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
st.subheader("Browse Galleries")

# Fetch all galleries first
all_galleries = []
try:
    res = requests.get(f"{API_BASE}/galleries/")
    if res.status_code == 200:
        all_galleries = res.json()
except requests.exceptions.ConnectionError:
    st.warning("Unable to connect to the API.")

if all_galleries:
    # Build dropdown options
    gallery_names = ["All Galleries"] + [g.get("name", "Unnamed") for g in all_galleries]
    selected = st.selectbox("Select a Gallery", gallery_names)

    if selected == "All Galleries":
        display_data = all_galleries
    else:
        display_data = [g for g in all_galleries if g.get("name") == selected]

    st.write(f"*{len(display_data)} gallery(ies)*")

    for gallery in display_data:
        with st.expander(f"{gallery.get('name', 'Unnamed')} — {gallery.get('wing', 'N/A')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"*Gallery ID:* {gallery.get('galleryID', 'N/A')}")
                st.write(f"*Wing:* {gallery.get('wing', 'N/A')}")
            with col2:
                st.write(f"*Capacity:* {gallery.get('artworkCapacity', 'N/A')} artworks")
                st.write(f"*Branch ID:* {gallery.get('branchID', 'N/A')}")
else:
    st.info("No galleries found.")