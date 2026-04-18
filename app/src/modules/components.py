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

def artist_dropdown(label="Select Artist", key="artist_selector"):
    """
    Fetches all artists and displays a dropdown with their full names.
    Returns the selected artistID.
    """
    try:
        res = requests.get(f"{API_BASE}/artists/")
        if res.status_code == 200:
            artists = res.json()
            if not artists:
                st.info("No artists found.")
                return None

            artist_options = {}
            for a in artists:
                if "firstName" in a and "lastName" in a:
                    full_name = f"{a['firstName']} {a['lastName']}"
                else:
                    full_name = a.get("name", f"Artist #{a['artistID']}")
                
                artist_options[full_name] = a["artistID"]

            selected_name = st.selectbox(label, options=list(artist_options.keys()), key=key)
            return artist_options[selected_name]
        
        st.error(f"Error: Backend returned {res.status_code}")
        return None
    except Exception as e:
        st.error(f"Failed to load artists: {e}")
        return None

def artifact_dropdown(label="Select Artifact", key="artifact_selector"):
    """
    Fetches all artifacts and returns the selected artifactID.
    """
    try:
        res = requests.get(f"{API_BASE}/artifacts")
        if res.status_code == 200:
            artifacts = res.json()
            if not artifacts:
                st.info("No artifacts available.")
                return None

            artifact_options = {
                f"{a.get('name', 'Unnamed')} | {a['artifactID']}": a["artifactID"] 
                for a in artifacts
            }

            selected_label = st.selectbox(label, options=list(artifact_options.keys()), key=key)
            return artifact_options[selected_label]
        
        st.error(f"Error: Backend returned {res.status_code}")
        return None
    except Exception as e:
        st.error(f"Failed to load artifacts: {e}")
        return None

def current_exhibits_dropdown(label="Select an Active Exhibit", key="exhibit_selector"):
    """
    Returns the exhibitID of the selected exhibit.
    """
    try:
        res = requests.get(f"{API_BASE}/exhibits/current")
        
        if res.status_code == 200:
            exhibits_data = res.json()
            
            if not exhibits_data:
                st.info("No active exhibits found.")
                return None

            # Dictionary mapping: "Label String" -> int(ID)
            # We assume your backend returns 'ex_id' or 'exhibitID'
            # (Double check your Flask SQL includes the ID column!)
            exhibit_options = {}
            for e in exhibits_data:
                # Fallback to a name if ID is missing for some reason
                eid = e.get('exhibitID') 
                display_text = f"{e['exhibit']} (@ {e['branchName']})"
                
                exhibit_options[display_text] = eid

            selected_label = st.selectbox(
                label, 
                options=list(exhibit_options.keys()), 
                key=key
            )
            
            # This returns the integer ID to your app.py
            return exhibit_options[selected_label]
        
        else:
            st.error(f"Error {res.status_code} fetching exhibits.")
            return None
            
    except Exception as e:
        st.error(f"Dropdown error: {e}")
        return None

def artifact_request_dropdown(label="Select a Loan Request", key="request_picker"):
    """
    Fetches all artifact requests and returns the selected requestID.
    """
    try:
        res = requests.get(f"{API_BASE}/requests")
        
        if res.status_code == 200:
            requests_data = res.json()
            
            if not requests_data:
                st.info("No artifact requests found.")
                return None

            # Create the mapping: "Label" -> ID
            request_options = {}
            for r in requests_data:
                # Format: "Request #101 (pending) - Starts: 2024-05-01"
                date_str = r.get('loanDateStart', 'N/A')
                # Cleaning up date string if it's a long timestamp
                short_date = date_str.split('T')[0] if 'T' in str(date_str) else date_str
                
                display_label = f"Request #{r['requestID']} ({r['status']})"
                request_options[display_label] = r['requestID']

            selected_label = st.selectbox(
                label, 
                options=list(request_options.keys()), 
                key=key
            )
            
            # Return the integer ID
            return request_options[selected_label]
        
        else:
            st.error(f"Requests Error: Backend returned {res.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Failed to load requests: {e}")
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
                        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/330px-Placeholder_view_vector.svg.png", use_container_width=True)
                else:
                    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Placeholder_view_vector.svg/330px-Placeholder_view_vector.svg.png", use_container_width=True)

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

def artifact_explorer_tab():
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
                    display_artifact_cards(data)
                else:
                    st.info("No artifacts found.")
            else:
                st.error(f"Error Fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")