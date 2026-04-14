import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 🎨")
st.write("### What would you like to do today?")

if st.button('Search & Filter Artifacts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/21_Search_Artifacts.py')

if st.button('Browse Galleries',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Galleries.py')

if st.button('Manage Artifact Requests',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Artifact_Requests.py')