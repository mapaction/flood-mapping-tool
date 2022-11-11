import streamlit as st
from sidebar_functions import add_logo, add_about

st.set_page_config(layout="wide")

add_logo("MA-logo.png")
add_about()
st.markdown("# Introduction")