import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Galleries & Expansion Projects")

tab1, tab2 = st.tabs(["Galleries", "Expansion Projects"])

# ---- Tab 1: Galleries (3.7.1, 3.7.2, 3.7.6) ---------------------------------
with tab1:
    # 3.7.1 – View gallery status
    st.subheader("Gallery Status")
    try:
        res = requests.get(f"{API_BASE}/galleries")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "branchName": "Branch",
                    "wing": "Wing",
                    "artworkCapacity": "Capacity",
                    "name": "Gallery Name",
                    "isInUse": "In Use",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No galleries found.")
        else:
            st.error(f"Error fetching galleries (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")

    st.divider()

    # 3.7.2 – Update gallery status
    st.subheader("Update Gallery Status")
    with st.form("update_gallery_form"):
        gallery_id = st.number_input("Gallery ID", min_value=1, step=1)
        new_status = st.selectbox("Set In Use", [True, False])
        submitted = st.form_submit_button("Update Status")
        if submitted:
            try:
                res = requests.put(
                    f"{API_BASE}/galleries/{gallery_id}",
                    json={"isInUse": new_status},
                )
                if res.status_code == 200:
                    st.success("Gallery status updated.")
                else:
                    st.error(f"Error updating gallery (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")

    st.divider()

    # 3.7.6 – Add a new gallery
    st.subheader("Add New Gallery")
    with st.form("add_gallery_form"):
        new_gal_id = st.number_input("Gallery ID", min_value=1, step=1, key="new_gal_id")
        new_gal_branch = st.number_input("Branch ID", min_value=1, step=1, key="new_gal_branch")
        new_gal_name = st.text_input("Gallery Name")
        new_gal_wing = st.text_input("Wing")
        new_gal_capacity = st.number_input("Artwork Capacity", min_value=1, step=1)
        add_submitted = st.form_submit_button("Add Gallery")
        if add_submitted:
            try:
                res = requests.post(
                    f"{API_BASE}/galleries",
                    json={
                        "galleryID": new_gal_id,
                        "branchID": new_gal_branch,
                        "isInUse": False,
                        "name": new_gal_name,
                        "wing": new_gal_wing,
                        "artworkCapacity": new_gal_capacity,
                    },
                )
                if res.status_code in (200, 201):
                    st.success("Gallery added successfully.")
                else:
                    st.error(f"Error adding gallery (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")


# ---- Tab 2: Expansion Projects (3.7.3, 3.7.4, 3.7.5) -------------------------
with tab2:
    # 3.7.3 – View expansion projects
    st.subheader("Active Expansion Projects")
    try:
        res = requests.get(f"{API_BASE}/projects")
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data).rename(columns={
                    "projectID": "Project ID",
                    "branchName": "Branch",
                    "description": "Description",
                    "status": "Status",
                    "costDollarAmount": "Cost ($)",
                    "contactName": "Contact",
                    "contactEmail": "Contact Email",
                    "contactPhone": "Contact Phone",
                })
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No expansion projects found.")
        else:
            st.error(f"Error fetching projects (HTTP {res.status_code})")
    except requests.exceptions.ConnectionError:
        st.warning("Unable to connect to the API.")

    st.divider()

    # 3.7.4 – Create a new expansion project
    st.subheader("Create Expansion Project")
    with st.form("create_project_form"):
        proj_branch = st.number_input("Branch ID", min_value=1, step=1, key="proj_branch")
        proj_desc = st.text_area("Description")
        proj_status = st.selectbox("Status", ["pending", "approved", "denied", "ongoing"])
        proj_cost = st.number_input("Cost ($)", min_value=0, step=1000)
        proj_contact = st.text_input("Contact Name")
        proj_phone = st.text_input("Contact Phone")
        proj_email = st.text_input("Contact Email")
        create_submitted = st.form_submit_button("Create Project")
        if create_submitted:
            try:
                res = requests.post(
                    f"{API_BASE}/projects",
                    json={
                        "headedByBranchID": proj_branch,
                        "description": proj_desc,
                        "status": proj_status,
                        "costDollarAmount": proj_cost,
                        "contactName": proj_contact,
                        "contactPhone": proj_phone,
                        "contactEmail": proj_email,
                    },
                )
                if res.status_code in (200, 201):
                    st.success("Expansion project created.")
                else:
                    st.error(f"Error creating project (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")

    st.divider()

    # 3.7.5 – Update expansion project status
    st.subheader("Update Project Status")
    with st.form("update_project_form"):
        upd_proj_id = st.number_input("Project ID", min_value=1, step=1, key="upd_proj_id")
        upd_status = st.selectbox(
            "New Status", ["pending", "approved", "denied", "ongoing"], key="upd_status"
        )
        update_submitted = st.form_submit_button("Update Status")
        if update_submitted:
            try:
                res = requests.put(
                    f"{API_BASE}/projects/{upd_proj_id}",
                    json={"status": upd_status},
                )
                if res.status_code == 200:
                    st.success("Project status updated.")
                else:
                    st.error(f"Error updating project (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")
