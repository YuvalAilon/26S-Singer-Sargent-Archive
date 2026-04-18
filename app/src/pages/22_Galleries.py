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
st.write("Browse galleries and check availability for your next exhibit.")

# Fetch all galleries first to populate dropdowns
all_galleries = []
try:
    res = requests.get(f"{API_BASE}/galleries/")
    if res.status_code == 200:
        all_galleries = res.json()
except requests.exceptions.ConnectionError:
    st.warning("Unable to connect to the API.")

if all_galleries:
    # Build filter options from the data
    gallery_names = ["Any"] + sorted(set(g.get("name", "Unnamed") for g in all_galleries))
    wings = ["Any"] + sorted(set(g.get("wing", "") for g in all_galleries if g.get("wing")))
    branch_ids = ["Any"] + sorted(set(str(g.get("branchID", "")) for g in all_galleries if g.get("branchID")))

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_name = st.selectbox("Gallery Name", gallery_names)
        selected_wing = st.selectbox("Wing", wings)
    with col2:
        selected_branch = st.selectbox("Branch ID", branch_ids)
        selected_capacity = st.number_input("Min Capacity (0 = any)", min_value=0, value=0, step=1)
    with col3:
        selected_availability = st.selectbox("Availability", ["All", "Available Only", "In Use Only"])

    # Decide which endpoint to use based on availability filter
    try:
        if selected_availability == "Available Only":
            res = requests.get(f"{API_BASE}/galleries/not-in-use")
        else:
            params = {}
            if selected_name != "Any":
                params["name"] = selected_name
            if selected_wing != "Any":
                params["wing"] = selected_wing
            if selected_branch != "Any":
                params["branchID"] = selected_branch
            res = requests.get(f"{API_BASE}/galleries/", params=params)

        if res.status_code == 200:
            display_data = res.json()

            # Filter capacity client-side (greater than)
            if selected_capacity > 0:
                display_data = [g for g in display_data if g.get("artworkCapacity", 0) >= selected_capacity]

            # For "In Use Only", get available gallery IDs and exclude them
            if selected_availability == "In Use Only":
                try:
                    avail_res = requests.get(f"{API_BASE}/galleries/not-in-use")
                    if avail_res.status_code == 200:
                        avail_ids = set((g.get("galleryID"), g.get("branchID")) for g in avail_res.json())
                        display_data = [g for g in display_data if (g.get("galleryID"), g.get("branchID")) not in avail_ids]
                except requests.exceptions.ConnectionError:
                    pass

            # Apply name/wing/branch filters for available-only (since that endpoint doesn't filter)
            if selected_availability == "Available Only":
                if selected_name != "Any":
                    display_data = [g for g in display_data if g.get("name") == selected_name]
                if selected_wing != "Any":
                    display_data = [g for g in display_data if g.get("wing") == selected_wing]
                if selected_branch != "Any":
                    display_data = [g for g in display_data if str(g.get("branchID")) == selected_branch]

            if display_data:
                st.write(f"**{len(display_data)} gallery(ies)**")
                for gallery in display_data:
                    gallery_id = gallery.get('galleryID', 'N/A')
                    with st.expander(f"{gallery.get('name', 'Unnamed')} — {gallery.get('wing', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"*Gallery ID:* {gallery_id}")
                            st.write(f"*Wing:* {gallery.get('wing', 'N/A')}")
                            st.write(f"*Capacity:* {gallery.get('artworkCapacity', 'N/A')} artworks")
                            st.write(f"*Branch ID:* {gallery.get('branchID', 'N/A')}")
                        with col2:
                            try:
                                detail_res = requests.get(f"{API_BASE}/galleries/{gallery_id}")
                                if detail_res.status_code == 200:
                                    detail = detail_res.json()
                                    exhibits = detail.get("Exhibits", [])
                                    if exhibits:
                                        st.warning(f"**In Use — {len(exhibits)} exhibit(s):**")
                                        for ex in exhibits:
                                            st.write(f"- {ex.get('name', 'Untitled')} ({ex.get('dateStart', 'N/A')} to {ex.get('dateEnd', 'Ongoing')})")
                                    else:
                                        st.success("Available — no active exhibits")
                            except requests.exceptions.ConnectionError:
                                st.write("Could not load exhibit info.")
            else:
                st.info("No galleries found matching your criteria.")
        else:
            st.error(f"Error fetching galleries (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")
else:
    st.info("No galleries found.")