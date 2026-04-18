import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from datetime import date
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Artifact Requests")

tab1, tab2, tab3 = st.tabs(["Track Requests", "New Request", "Update Status"])

# ------ Tab 1: Track Requests -------------------------------------------
with tab1:
    st.subheader("Current Artifact Requests")

    view_mode = st.radio("View", ["All Requests", "Future Returns", "By Exhibit"], horizontal=True)

    if view_mode == "All Requests":
        try:
            res = requests.get(f"{API_BASE}/requests")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "requestID": "Request ID",
                        "exhibitID": "Exhibit ID",
                        "loaningDonorID": "Donor ID",
                        "requestingEmployeeID": "Requested By",
                        "loanDateStart": "Loan Start",
                        "loanDateEnd": "Loan End",
                        "status": "Status",
                    })
                    st.write(f"**{len(data)} request(s) found**")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No requests found.")
            else:
                st.error(f"Error fetching requests (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

    elif view_mode == "Future Returns":
        try:
            res = requests.get(f"{API_BASE}/requests/future-returns")
            if res.status_code == 200:
                data = res.json()
                if data:
                    df = pd.DataFrame(data).rename(columns={
                        "requestID": "Request ID",
                        "exhibitID": "Exhibit ID",
                        "loaningDonorID": "Donor ID",
                        "requestingEmployeeID": "Requested By",
                        "loanDateStart": "Loan Start",
                        "loanDateEnd": "Loan End",
                        "status": "Status",
                    })
                    st.write(f"**{len(data)} upcoming return(s)**")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No upcoming returns.")
            else:
                st.error(f"Error fetching returns (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

    elif view_mode == "By Exhibit":
        exhibit_id = st.number_input("Exhibit ID", min_value=1, step=1, key="exhibit_filter")
        if st.button("Search", key="search_exhibit"):
            try:
                res = requests.get(f"{API_BASE}/requests/by-exhibit/{exhibit_id}")
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        df = pd.DataFrame(data).rename(columns={
                            "requestID": "Request ID",
                            "exhibitID": "Exhibit ID",
                            "loaningDonorID": "Donor ID",
                            "requestingEmployeeID": "Requested By",
                            "loanDateStart": "Loan Start",
                            "loanDateEnd": "Loan End",
                            "status": "Status",
                        })
                        st.write(f"**{len(data)} request(s) for exhibit {exhibit_id}**")
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.info(f"No requests found for exhibit {exhibit_id}.")
                else:
                    st.error(f"Error fetching requests (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")

    st.divider()
    st.subheader("View Artifacts in a Request")
    request_id_lookup = st.number_input("Request ID", min_value=1, step=1, key="req_artifacts")
    if st.button("View Artifacts", key="view_req_artifacts"):
        try:
            res = requests.get(f"{API_BASE}/requests/{request_id_lookup}/artifacts")
            if res.status_code == 200:
                data = res.json()
                if data:
                    for item in data:
                        with st.expander(f"{item.get('name', 'Untitled')} ({item.get('createdYear', 'N/A')})"):
                            col_img, col_info = st.columns([1, 2])
                            with col_img:
                                if item.get('imageURL'):
                                    st.image(item['imageURL'], use_container_width=True)
                                else:
                                    st.write("*No image available*")
                            with col_info:
                                st.write(f"**Style:** {item.get('style', 'N/A')}")
                                st.write(f"**Medium:** {item.get('medium', 'N/A')}")
                                st.write(f"**Condition:** {item.get('artifactCondition', 'N/A')}")
                else:
                    st.info("No artifacts linked to this request.")
            else:
                st.error(f"Error fetching artifacts (HTTP {res.status_code})")
        except requests.exceptions.ConnectionError:
            st.warning("Unable to connect to the API.")

# ------ Tab 2: New Request -----------------------------------------
with tab2:
    st.subheader("Create a New Artifact Request")

    request_type = st.radio("Request Type", ["From Branch", "From Donor/Patron"], horizontal=True)

    with st.form("new_request_form"):
        col1, col2 = st.columns(2)

        with col1:
            exhibit_id = st.number_input("For Exhibit ID", min_value=1, step=1)
            loan_start = st.date_input("Loan Start Date", value=date.today())

        with col2:
            if request_type == "From Donor/Patron":
                donor_id = st.number_input("Donor ID", min_value=1, step=1)
            else:
                donor_id = None
                st.info("Branch-to-branch request (no donor)")
            loan_end = st.date_input("Loan End Date")

        st.divider()
        artifact_ids_input = st.text_input("Artifact IDs (comma-separated)")

        submitted = st.form_submit_button("Submit Request", type="primary", use_container_width=True)

        if submitted:
            payload = {
                "exhibitID": exhibit_id,
                "loaningDonorID": donor_id,
                "requestingEmployeeID": st.session_state.get('employee_id', 3326),
                "loanDateStart": str(loan_start),
                "loanDateEnd": str(loan_end),
                "status": "pending",
            }
            try:
                res = requests.post(f"{API_BASE}/requests", json=payload)
                if res.status_code in (200, 201):
                    st.success("Request created.")
                else:
                    st.error(f"Error creating request (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")

# ------ Tab 3: Update Status --------------------------------------------------
with tab3:
    st.subheader("Update Request Status")

    with st.form("update_request_form"):
        request_id = st.number_input("Request ID", min_value=1, step=1)
        new_status = st.selectbox("New Status",
                                   ["pending", "approved", "denied", "ongoing"])
        submitted = st.form_submit_button("Update Status", type="primary", use_container_width=True)

        if submitted:
            try:
                res = requests.put(
                    f"{API_BASE}/requests/{request_id}",
                    json={"status": new_status},
                )
                if res.status_code == 200:
                    st.success(f"Request {request_id} updated to '{new_status}'.")
                else:
                    st.error(f"Error updating request (HTTP {res.status_code})")
            except requests.exceptions.ConnectionError:
                st.warning("Unable to connect to the API.")