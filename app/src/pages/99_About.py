import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    The Singer-Sargent Archives is a data-driven application designed to help museums 
    keep track of their artifacts and galleries. At any point, a museum is planning many 
    exhibits and has many artworks on loan, so it is important to have an easy way to keep 
    track of the museum's inventory at all times.

    Stay tuned for more information and features to come!
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
