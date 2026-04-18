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

st.title("Manage Artifacts")

tab1, tab2, tab3, tab4 = st.tabs(["View Sets", "View Artifacts In Set", "Create New Set", "Add / Remove Artifacts"])

#------ Tab 1: View Artifacts In Set -------------------------------------------------------------
with tab1:
    st.header("Artifact Sets Explorer")

    selected_group_id = artifact_group_dropdown(key="explorer_set_picker")

    if selected_group_id:
        if st.button("Load Artifacts", type="primary"):
            try:
                res = requests.get(f"{API_BASE}/artifact_groups/{selected_group_id}/artifacts")
                
                if res.status_code == 200:
                    artifacts = res.json()
                    
                    display_artifact_cards(artifacts)
                else:
                    st.error("Error: Could not retrieve artifacts for this group.")
            except Exception as e:
                st.error(f"Connection error: {e}")
#------ Tab 2: View Set ----------------------------------------
with tab2:
    st.subheader("Existing Artifact Sets")
    try:
        res = requests.get(f"{API_BASE}/artifact_groups/")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "artifactSetID": "Set ID",
                    "name": "Set Name",
                    "description": "Description",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No artifact sets found.")
        else: 
            st.error(f"Error fetching sets (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")

#------ Tab 3: Create New Set -----------------------------------------------
with tab3:
    st.subheader("Create a New Artifact Set")

    with st.form("create_set_form"):
        set_id = st.number_input("Set ID*", min_value=1, step=1)
        set_name = st.text_input("Set Name*")
        set_description = st.text_area("Description")

        submitted = st.form_submit_button("Create Set", type="primary", use_container_width=True)

        if submitted:
            if not set_name:
                st.error("Set name is required.*")
            else:
                payload = {
                    "artifactSetID": set_id,
                    "name": set_name,
                    "description": set_description or None,
                }
                try:
                    res = requests.post(f"{API_BASE}/artifact_groups/", json=payload)
                    if res.status_code in (200, 201):
                        st.success(f"Created set '{set_name}'.")
                    else:
                        st.error(f"Error creating set (HTTP {res.status_code})")
                except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")

# ------ Tab 4: Add / Remove Artifacts 
with tab4:
    st.subheader("Add or Remove Artifacts from a Set ")

    col1, col2 = st.columns(2)
    with col1:
        set_id = artifact_group_dropdown(key="set_picker_add_remove_artifact")
    with col2:
        artifact_id = st.number_input("Artifact ID", min_value=1, step=1)

    col_add, col_remove = st.columns(2)

    with col_add:
        if st.button("Add to Set", type="primary", use_container_width=True):
            try:
                res = requests.post(f"{API_BASE}/artifacts/{artifact_id}/artifact_group", 
                                        json={"artifactSetID": set_id})
                if res.status_code in (200, 201):
                        st.success(f"Added artifact {artifact_id} to set {set_id}.")
                else:
                        st.error(f"Error adding artifact (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")

    with col_remove:
        if st.button("Remove from Set", use_container_width=True):
            try:
                res = requests.delete(f"{API_BASE}/artifacts/{artifact_id}/artifact_group", 
                                      json={"artifactSetID": set_id})
                if res.status_code == 200:
                        st.success(f"Removed artifact {artifact_id} from set {set_id}.")
                else:
                        st.error(f"Error removing artifact (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")

                    


                    
