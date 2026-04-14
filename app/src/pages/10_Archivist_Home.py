import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 📜")
st.write("### What would you like to do today?")

if st.button('Add New Artifact',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_Add_Artifact.py')

if st.button('Manage Existing Artifacts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Manage_Artifacts.py')

if st.button('Manage Artifact Sets',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_Artifact_Sets.py')