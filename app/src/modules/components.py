import streamlit as st
import requests

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