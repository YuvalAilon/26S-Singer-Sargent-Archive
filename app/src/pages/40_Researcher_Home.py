import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 🔬")
st.write("### What would you like to explore today?")

if st.button('Browse the Collection',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/41_Browse_Collection.py')

if st.button('View Current Exhibits',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/42_Exhibits.py')

if st.button('Museum Statistics',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/43_Museum_Stats.py')