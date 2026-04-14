# Sidebar navigation for The Singer-Sargent Archives
# Controls which links appear based on user role

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def about_page_nav():
    st.sidebar.page_link("pages/99_About.py", label="About", icon="📄")


# ---- Role: archivist --------------------------------------------------------

def archivist_home_nav():
    st.sidebar.page_link("pages/10_Archivist_Home.py", label="Archivist Home", icon="📜")


def add_artifact_nav():
    st.sidebar.page_link("pages/11_Add_Artifact.py", label="Add Artifact", icon="📁")


def manage_artifacts_nav():
    st.sidebar.page_link("pages/12_Manage_Artifacts.py", label="Manage Artifacts", icon="✏️")


def artifact_sets_nav():
    st.sidebar.page_link("pages/13_Artifact_Sets.py", label="Artifact Sets", icon="📦")


# ---- Role: curator ----------------------------------------------------------

def curator_home_nav():
    st.sidebar.page_link("pages/20_Curator_Home.py", label="Curator Home", icon="🎨")


def search_artifacts_nav():
    st.sidebar.page_link("pages/21_Search_Artifacts.py", label="Search Artifacts", icon="🔍")


def galleries_nav():
    st.sidebar.page_link("pages/22_Galleries.py", label="Galleries", icon="🏛️")


def artifact_requests_nav():
    st.sidebar.page_link("pages/23_Artifact_Requests.py", label="Artifact Requests", icon="📋")


# ---- Role: director ---------------------------------------------------------

def director_home_nav():
    st.sidebar.page_link("pages/30_Director_Home.py", label="Director Home", icon="👔")


def donors_nav():
    st.sidebar.page_link("pages/31_Donors.py", label="Donors", icon="💰")


def loans_returns_nav():
    st.sidebar.page_link("pages/32_Loans_Returns.py", label="Loans & Returns", icon="📅")


def galleries_expansion_nav():
    st.sidebar.page_link("pages/33_Galleries_Expansion.py", label="Galleries & Expansion", icon="🏗️")


# ---- Role: researcher -------------------------------------------------------

def researcher_home_nav():
    st.sidebar.page_link("pages/40_Researcher_Home.py", label="Researcher Home", icon="🔬")


def browse_collection_nav():
    st.sidebar.page_link("pages/41_Browse_Collection.py", label="Browse Collection", icon="🖼️")


def exhibits_nav():
    st.sidebar.page_link("pages/42_Exhibits.py", label="Exhibits", icon="🗓️")


def museum_stats_nav():
    st.sidebar.page_link("pages/43_Museum_Stats.py", label="Museum Stats", icon="📊")


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    """

    st.sidebar.image("assets/logo.png", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "archivist":
            archivist_home_nav()
            add_artifact_nav()
            manage_artifacts_nav()
            artifact_sets_nav()

        if st.session_state["role"] == "curator":
            curator_home_nav()
            search_artifacts_nav()
            galleries_nav()
            artifact_requests_nav()

        if st.session_state["role"] == "director":
            director_home_nav()
            donors_nav()
            loans_returns_nav()
            galleries_expansion_nav()

        if st.session_state["role"] == "researcher":
            researcher_home_nav()
            browse_collection_nav()
            exhibits_nav()
            museum_stats_nav()

    about_page_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")