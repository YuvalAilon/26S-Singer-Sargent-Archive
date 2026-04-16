##################################################
# The Singer-Sargent Archives
# Main entry point - Role selection
##################################################

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('🏛️ The Singer-Sargent Archives')
st.write('#### Welcome! Please select your role to continue.')

if st.button("Act as Veronica-Elizabeth, an Archivist",
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'archivist'
    st.session_state['first_name'] = 'Veronica-Elizabeth'
    st.session_state['employee_id'] = 3324
    logger.info("Logging in as Archivist Persona")
    st.switch_page('pages/10_Archivist_Home.py')

if st.button('Act as Watney, a Curator',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'curator'
    st.session_state['first_name'] = 'Watney'
    st.session_state['employee_id'] = 3326
    logger.info("Logging in as Curator Persona")
    st.switch_page('pages/20_Curator_Home.py')

if st.button('Act as Marshal, a Director',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'director'
    st.session_state['first_name'] = 'Marshal'
    st.session_state['employee_id'] = 3327
    logger.info("Logging in as Director Persona")
    st.switch_page('pages/30_Director_Home.py')

if st.button('Act as Isabella, a Researcher',
             type='primary',
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'researcher'
    st.session_state['first_name'] = 'Isabella'
    logger.info("Logging in as Researcher Persona")
    st.switch_page('pages/40_Researcher_Home.py')

