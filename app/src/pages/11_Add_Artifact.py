import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Add New Artifact")

tab1,  tab2 = st.tabs(["Single Artifact", "Bulk Add"])

# ------ Tab 1 : Add Single Artifact -------------------

with tab1:
    st.subheader("Add a Single Artifact")

    with st.form("add_artifact_form"):
        col1, col2 = st.columns(2)

        with col1:
            artifact_id = st.number_input("Artifact ID *", min_value=1, step=1)
            name = st.text_input("Artifact Name *")
            medium = st.text_input("Medium")
            style = st.text_input("Style")
            created_year = st.number_input("Year Created", 
                                           min_value=0, max_value=2026, value=1900, step=1)
            condition = st.selectbox("Condition", 
                                        ["pristine", "good", "fair", "poor", "requires restoration" ])
        with col2:
            artist_id = st.number_input("Artist ID", min_value=0, value=0, step=1)
            description = st.text_area("Description")
            image_url = st.text_input("Image URL")
            exhibit_id = st.number_input("Display in Exhibit ID (0 = none)", min_value=0, value=0, step=1)

        submitted = st.form_submit_button("Add Artifact", type="primary", use_container_width=True)

        if submitted:
            if not name:
                st.error("Artifact name is required.")
            else:
                payload = {
                "artifactID": artifact_id,
                "name": name, 
                "medium": medium or None,
                "style": style or None,
                "createdYear": created_year if created_year > 0 else None,
                "artifactCondition": condition, 
                "artistID": artist_id if artist_id > 0 else None,
                "description": description or None,
                "imageURL": image_url or None,
                "displayedInExhibitID": exhibit_id if exhibit_id > 0 else None, 
                "archivedByEmployeeID": st.session_state.get('employee_id', 3324),
                }

                try:
                    res = requests.post(f"{API_BASE}/artifacts", json=payload)
                    if res.status_code in (200, 201):
                        st.success(f"Added '{name}' to the collection.")
                    else:
                        st.error(f"Error adding artifact (HTTP {res.status_code})")
                except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")
# ------ Tab 2: Bulk Add ------------------------------------------------------------
with tab2:
    st.subheader("Bulk Add Artifacts with Shared Attributes")

    with st.form("bulk_add_form"):
        st.write("Shared Fields*")
        col1, col2 = st.columns(2)

        with col1:
            bulk_artist_id = st.number_input("Artist ID", min_value=0, value=0, step=1, key="bulk_artist")
            bulk_style = st.text_input("Style", key="bulk_style")
            bulk_medium = st.text_input("Medium", key="bulk_medium")

        with col2:
            bulk_year = st.number_input("Year Created", min_value=0, value=1900, step=1, key="bulk_year")
            bulk_condition = st.selectbox("Condition",
                                             ["pristine", "good", "fair", "poor", "requires restoration"],
                                             key="bulk_condition")
        st.divider()
        st.write("Artifact Names* (one per line)")
        artifact_names = st.text_area("Names", height=150)

        bulk_submitted = st.form_submit_button("Bulk Add", type="primary", use_container_width=True)

        if bulk_submitted:
            names = [n.strip() for n in artifact_names.split("\n") if n.strip()]
            if not names:
                st.error("Enter at least one artifact name.")
            else:
                success_count = 0
                for artifact_name in names:
                    payload = {
                        "name": artifact_name,
                        "artistID": bulk_artist_id if bulk_artist_id > 0 else None, 
                        "style": bulk_style or None,
                        "medium": bulk_medium or None,
                        "createdYear": bulk_year if bulk_year > 0 else None,
                        "artifactCondition": bulk_condition,
                        "archivedByEmployeeID": st.session_state.get("employee_id", 3324)
                    }
                    try: 
                        res = requests.post(f"{API_BASE}/artifacts", json=payload)
                        if res.status_code in (200, 201):
                            success_count += 1
                    except requests.exceptions.ConnectionError:
                        pass

                if success_count > 0:
                    st.success(f"Added {success_count} of {len(names)} artifacts.")
                else:
                    st.warning("Unable to connect to the API.")







