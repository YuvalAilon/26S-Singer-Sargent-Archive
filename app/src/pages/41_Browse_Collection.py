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

st.title("Browse the Collection")

tab1, = st.tabs(["The Museum's Complete Collection"])


# ---- Tab 1: Search The Complete Collection ----------------------------------------------
with tab1:
   artifact_explorer_tab()