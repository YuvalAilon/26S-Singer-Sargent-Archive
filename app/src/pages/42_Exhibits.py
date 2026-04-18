import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Current Exhibits")

st.write("Exhibits that are open today or have no scheduled end date.")

city_filter = st.text_input("Filter by city (optional)", value="")

params = {}
if city_filter.strip():
    params["city"] = city_filter.strip()

try:
    res = requests.get(f"{API_BASE}/exhibits/current", params=params)
    if res.status_code == 200:
        data = res.json()
        if not data:
            st.info("No current exhibits found.")
        else:
            df = pd.DataFrame(data).rename(columns={
                "branchName": "Museum",
                "street": "Street",
                "city": "City",
                "state": "State",
                "zip": "Zip",
                "contactPhone": "Phone",
                "exhibit": "Exhibit",
                "name": "Exhibit",
                "dateStart": "Starts",
                "dateEnd": "Ends",
            })
            preferred = [
                "Museum", "Exhibit", "Starts", "Ends",
                "Street", "City", "State", "Zip", "Phone",
            ]
            ordered = [c for c in preferred if c in df.columns]
            extras = [c for c in df.columns if c not in ordered]
            df = df[ordered + extras]
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error(f"Error fetching exhibits (HTTP {res.status_code})")
except requests.exceptions.ConnectionError:
    st.warning("Unable to connect to the API.")
