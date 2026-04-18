import logging
logger = logging.getLogger(__name__)
 
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Manage Artifacts")

tab1, tab2, tab3 = st.tabs(["Browse All", "Missing Information", "Edit / Delete"])

# ------ Tab 1 : Browse All Artifacts ---------------------------------------------
with tab1:
    st.subheader("All Artifacts")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        filter_artifact_name = st.text_input("Artifact Name", key="browse_artifact_name")
    with col2:
        filter_artist_name = st.text_input("Artist Name", key="browse_artist_name")
    with col3:
        filter_style = st.text_input("Style", key="browse_style")
    with col4:
        filter_date_before = st.text_input("Year Before", key="browse_year_before")
    with col5:
        filter_date_after = st.text_input("Year After", key="browse_year_after")
    
    if st.button("Search", type="primary", key="browse_search"):
        try:
            params = {}
            if filter_artifact_name:
                params["name"] = filter_artifact_name
            if filter_artist_name:
                params["artistName"] = filter_artist_name
            if filter_style:
                params["style"] = filter_style
            if filter_date_before:
                params["dateBefore"] = filter_date_before
            if filter_date_after:
                params["dateAfter"] = filter_date_after
            res = requests.get(f"{API_BASE}/artifacts/filter", params=params)
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data)

                    cols_to_keep = ["artifactID", "name", "style", "medium", "createdYear", "artifactCondition"]
                    df = df[cols_to_keep]
                    
                    df.rename(columns={
                        "artifactID": "ID",
                        "name": "Name",
                        "style": "Style",
                        "medium": "Medium",
                        "createdYear": "Year",
                        "artifactCondition": "Condition",
                    })
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No artifacts found.")
            else:
                st.error(f"Error Fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

# ------ Tab 2: Missing Information --------------------------------------------
with tab2:
    st.subheader("Artifacts with Missing Information")

    if st.button("Find Incomplete Artifacts", type="primary", key="find_missing"):
        try:
            res = requests.get(f"{API_BASE}/artifacts/missing_info")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "artifactID": "ID",
                        "name": "Name",
                        "description": "Description",
                        "style": "Style",
                        "createdYear": "Year",
                        "artistID": "Artist ID",
                    })
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.success("All artifacts have complete information.")
            else:
                st.error(f"Error fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")
#------ Tab3: Edit / Delete ----------------------------------------------------
with tab3:
    st.subheader("Edit or Delete an Artifact")

    artifact_id = st.number_input("Artifact ID", min_value=1, step=1)

    if st.button("Load Artifact", key="load_artifact"):
        try:
            res = requests.get(f"{API_BASE}/artifacts/{artifact_id}")
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list) and data:
                    st.session_state["editing_artifact"] = data[0]
                elif isinstance(data, dict):
                    st.session_state["editing_artifact"] = data
                else:
                    st.error("Artifact not found.")
            else:
                st.error(f"Artifact not found (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")
    if "editing_artifact" in st.session_state:
        artifact = st.session_state["editing_artifact"]

        with st.form("edit_artifact_form"):
            col1, col2 = st.columns(2)

            with col1:
                edit_name = st.text_input("Name", value=artifact.get("name", ""))
                edit_medium = st.text_input("Medium", value=artifact.get("medium", "") or "")
                edit_style = st.text_input("Style", value=artifact.get('style', "") or "")
                edit_year = st.number_input("Year Created",
                                            value=artifact.get('createdYear', 0) or 0,
                                            min_value=0, max_value=2026)
            with col2:
                conditions = ["pristine", "good", "fair", "poor", "requires restoration"]
                current_cond = artifact.get("artifactCondition", "good")
                cond_idx = conditions.index(current_cond) if current_cond in conditions else 1
                edit_condition = st.selectbox("Condition", conditions, index=cond_idx)
                edit_description = st.text_area("Description",
                                                value=artifact.get("description", "") or "")
                edit_image = st.text_input("Image URL",
                                           value=artifact.get("imageURL", "") or "")
                
            col_save, col_delete = st.columns(2)

            with col_save:
                save = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
            with col_delete:
                delete = st.form_submit_button("Delete Artifact", use_container_width=True)
            
            if save:
                payload = {
                    "name": edit_name,
                    "condition": edit_condition,
                }
                try:
                    res = requests.put(f"{API_BASE}/artifacts/{artifact_id}", json=payload)
                    if res.status_code == 200:
                        st.success("Artifact updated.")
                        del st.session_state["editing_artifact"]
                    else:
                        st.error(f"Error updating artifact (HTTP {res.status_code})")
                except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")

            if delete:
                try:
                    res = requests.delete(f"{API_BASE}/artifacts/{artifact_id}")
                    if res.status_code == 200:
                        st.success("Artifact deleted.")
                        del st.session_state["editing_artifact"]
                    else:
                        st.error(f"Error deleting artifact (HTTP {res.status_code})")
                except requests.exceptions.ConnectionError:
                    st.warning("Unable to connect to the API.")


            
                
                

                    

                    

