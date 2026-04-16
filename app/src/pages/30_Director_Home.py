import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}! 👔")
st.write("### What would you like to do today?")

if st.button('Manage Donors',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Donors.py')

if st.button('Track Loans & Returns',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Loans_Returns.py')

if st.button('Galleries & Expansion Projects',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Galleries_Expansion.py')
