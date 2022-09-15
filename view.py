import streamlit as st

st.set_page_config(
    page_title="MISEM",
    page_icon="🧊",
    layout="wide",
)

hide_decoration_bar_style = """
    <style>
        header {visibility: hidden;}
        body {
    line-break: anywhere;
    }
    </style>
"""
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

from pages import dashboard
from pages import home

if "page" not in st.session_state:
    st.session_state.page = "home"
if "reference_text" not in st.session_state:
    st.session_state.reference_text = """reference text"""
if "inference_text" not in st.session_state:
    st.session_state.inference_text = """inference text"""
if "distance_threshold" not in st.session_state:
    st.session_state.distance_threshold = 0.9
if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = 0

st.title("MISEM")
st.caption(
    "MISEM is a tool for comparing two texts based on their topics and visualizing the results."
)

if st.session_state.page == "home":
    home.run()
elif st.session_state.page == "dashboard":
    dashboard.run()
else:
    dashboard.run()
