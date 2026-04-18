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
    

def display_artifact_cards(artifacts_json):
    """
    Takes a list of artifact dictionaries and renders them as pretty cards.
    """
    if not artifacts_json:
        st.info("No artifacts to display.")
        return

    for art in artifacts_json:
        with st.container(border=True):
            img_col, text_col = st.columns([1, 2])
            
            with img_col:
                image_url = art.get("imageURL")
                
                if image_url and isinstance(image_url, str) and image_url.startswith(("http://", "https://")):
                    try:
                        st.image(image_url, use_container_width=True)
                    except Exception:
                        st.image("https://via.placeholder.com/300x200?text=Link+Broken", use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x200?text=No+Image+Available", use_container_width=True)

            with text_col:
                st.subheader(art.get("name", "Unnamed Artifact"))
                
                # Metadata Grid
                m1, m2 = st.columns(2)
                m1.write(f"**Style:** {art.get('style', 'Unknown')}")
                m1.write(f"**Year:** {art.get('createdYear', 'N/A')}")
                m2.write(f"**Medium:** {art.get('medium', 'N/A')}")
                m2.write(f"**Condition:** {art.get('artifactCondition', 'N/A')}")
                
                # Expandable Details
                if art.get("description"):
                    with st.expander("Read Description"):
                        st.write(art["description"])