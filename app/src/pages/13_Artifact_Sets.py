import logging
logger = logging.getLogger(__name__)
 
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

def artifact_group_dropdown(label="Select Artifact Set", key="group_selector"):
    """
    Reusable dropdown component that fetches artifact groups from the API.
    Returns the selected groupID or None if no groups exist.
    """
    try:
        res = requests.get(f"{API_BASE}/artifact_groups")
        if res.status_code == 200:
            groups = res.json()
            if not groups:
                st.info("No artifact sets available.")
                return None
            
            # Map Name -> ID for the UI
            group_map = {g["name"]: g["artifactSetID"] for g in groups}
            
            selected_name = st.selectbox(label, options=list(group_map.keys()), key=key)
            return group_map[selected_name]
        else:
            st.error(f"Failed to load groups (HTTP {res.status_code})")
            return None
    except Exception as e:
        st.error(f"Dropdown Error: {e}")
        return None

st.title("Manage Artifacts")

tab1, tab2, tab3, tab4 = st.tabs(["View Sets", "View Artifacts In Set", "Create New Set", "Add / Remove Artifacts"])

#------ Tab 1: View Set -------------------------------------------------------------
with tab1:
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
#------ Tab 2: View Artifacts In Set ----------------------------------------
with tab2:
    st.header("Artifact Sets Explorer")

    selected_group_id = artifact_group_dropdown(key="explorer_set_picker")

    if selected_group_id:
        if st.button("Load Artifacts", type="primary"):
            try:
                res = requests.get(f"{API_BASE}/artifact_groups/{selected_group_id}/artifacts")
                
                if res.status_code == 200:
                    artifacts = res.json()
                    
                    if not artifacts:
                        st.warning("This set is currently empty.")
                    else:
                        # Display each artifact in a clean card format
                        for art in artifacts:
                            with st.container(border=True):
                                img_col, text_col = st.columns([1, 2])
                                
                                with img_col:
                                    # Check for imageURL and display if it exists
                                    if art.get("imageURL"):
                                        st.image(art["imageURL"], use_container_width=True)
                                    else:
                                        # Helpful placeholder so the UI doesn't look broken
                                        st.image("https://via.placeholder.com/300x200?text=No+Image+Available", use_container_width=True)
                                
                                with text_col:
                                    st.subheader(art.get("name", "Unnamed Artifact"))
                                    
                                    # Organized Metadata
                                    meta_cols = st.columns(2)
                                    meta_cols[0].write(f"**Style:** {art.get('style', 'Unknown')}")
                                    meta_cols[0].write(f"**Year:** {art.get('createdYear', 'N/A')}")
                                    meta_cols[1].write(f"**Medium:** {art.get('medium', 'N/A')}")
                                    meta_cols[1].write(f"**Condition:** {art.get('artifactCondition', 'N/A')}")
                                    
                                    if art.get("description"):
                                        with st.expander("Read Description"):
                                            st.write(art["description"])
                else:
                    st.error("Error: Could not retrieve artifacts for this group.")
            except Exception as e:
                st.error(f"Connection error: {e}")
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

                    


                    
